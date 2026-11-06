import logging

from fastapi import APIRouter, status, Request

from mcp_gateway.domain.external.model import HealthResponse, ServiceRequest, ServiceResponse

from mcp_gateway.domain.usecase.health import HealthUseCase
from mcp_gateway.domain.usecase.register import RegisteredServicesUseCase

from mcp_gateway.domain.external.error_response import AppError

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Health"],
)

#----------------------------------------------
# Registered health endpoint for the gateway
@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check gateway health",
)

#----------------------------------------------
# Health check endpoint for the gateway
def get_health() -> HealthResponse:
    use_case = HealthUseCase()
    result = use_case.execute()

    return HealthResponse(message=result.message)

#----------------------------------------------
# Registered services endpoint for the gateway
@router.post(
    "/v1/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post registered services",
)
async def get_registered_services(payload: ServiceRequest, request: Request) -> ServiceResponse:
    logger.info("Executing get_registered_services endpoint : payload=%s", payload)
    with tracer.start_as_current_span("router.get_registered_service") as span:
        try:
            repo = request.app.state.container.mcp_server_repository
            use_case = RegisteredServicesUseCase(repo)
            
            result = await use_case.add_registered_service(payload)
            message = f"Service {result.name} added successfully"

            return ServiceResponse(message=message, service=result)
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))

            logger.error(f"Error adding registered service: {e}")
            raise AppError(
                message=f"Error adding registered service: {e}",
                error="ERROR",
                status_code=500,
            ) from e

#----------------------------------------------
# Get registered services endpoint for the gateway
@router.get(
    "/v1/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get registered services",
)
async def get_registered_service(payload: ServiceRequest, request: Request) -> ServiceResponse:
    logger.info("Executing get_registered_service endpoint : payload=%s", payload)
    with tracer.start_as_current_span("router.get_registered_service") as span:
        try:
            repo = request.app.state.container.mcp_server_repository
            use_case = RegisteredServicesUseCase(repo)
            
            result = await use_case.get_registered_service(payload)
            message = f"Service {result.name} retrieved successfully"

            return ServiceResponse(message=message, service=result)
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))

            logger.error(f"Error retrieving registered service: {e}")
            raise AppError(
                message=f"Error retrieving registered service: {e}",
                error="ERROR",
                status_code=500,
            ) from e