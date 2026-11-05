import logging

from fastapi import APIRouter, status

from mcp_gateway.domain.external.model import HealthResponse
from mcp_gateway.domain.usecase.health import HealthUseCase

from mcp_gateway.domain.external.model import ServiceResponse
from mcp_gateway.domain.usecase.register import RegisteredServicesUseCase

from opentelemetry import trace

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
    status_code=status.HTTP_200_OK,
    summary="Post registered services",
)
def get_registered_services() -> ServiceResponse:
    with tracer.start_as_current_span("router.get_registered_service") as span:
        use_case = RegisteredServicesUseCase()
        result = use_case.add_registered_service()
        
        message = f"Service {result.name} added successfully"
        

        return ServiceResponse(message=message, service=result)

@router.get(
    "/v1/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get registered services",
)
def get_registered_service() -> ServiceResponse:
    with tracer.start_as_current_span("router.get_registered_service") as span:
        use_case = RegisteredServicesUseCase()
        result = use_case.get_registered_service()
        
        message = f"Service {result.name} retrieved successfully"
        
        
        return ServiceResponse(message=message, service=result)