import logging
import asyncio
from contextlib import asynccontextmanager
from mcp_gateway.api.http.middleware.middleware_auth import RequestContextMiddleware
from mcp_gateway.api.http.middleware.middleware_metric import PrometheusMiddleware

from fastapi import FastAPI
from opentelemetry import trace

from mcp_gateway.config.settings import settings
from mcp_gateway.infrastructure.observability.logger import setup_logger
from mcp_gateway.infrastructure.observability.tracer import setup_tracer

from mcp_gateway.api.http.router.endpoint import router as health_router
from mcp_gateway.api.http.router.endpoint import router as service_router

# Setup logging and tracing for the application
setup_logger(
    settings.LOG_LEVEL,
    settings.APP_NAME,
    settings.OTEL_STDOUT_LOG_GROUP,
    settings.LOG_GROUP,
)

# Setup tracing for the application
setup_tracer(settings.APP_NAME, settings.OTEL_EXPORTER_OTLP_ENDPOINT)

# Initialize logger and tracer for the application
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

# Application lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("**** Starting up the application...")
    logger.info(f"**** Metrics server at {settings.METRICS_HOST}:{settings.METRICS_PORT}")
    logger.info(f"**** HTTP server at {settings.HOST}:{settings.PORT}")
    yield
    logger.info("**** Shutting down the application...")
    await asyncio.sleep(1)
    logger.info("**** Shutdown complete.")

# Create and configure the FastAPI application instance
def create_app() -> FastAPI:
    logger.info("Initializing server resources")

    app = FastAPI(
        title="MCP Gateway",
        description="Gateway between MCP clients and internal MCP servers.",
        version=settings.VERSION,
        lifespan=lifespan,
    )

    app.include_router(health_router)
    app.include_router(service_router)
    
    app.add_middleware(PrometheusMiddleware)
    app.add_middleware(RequestContextMiddleware)  # Assuming you have an AuthMiddleware defined and imported at the top
    return app