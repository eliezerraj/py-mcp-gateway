import logging

from mcp_gateway.domain.external.model import ServiceRequest
from mcp_gateway.domain.model.service import Service

from opentelemetry import trace

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class RegisteredServicesUseCase:
    
    def get_registered_service(self) -> Service:
        with tracer.start_as_current_span("usecase.get_registered_service") as span:
            logger.info("Executing get_registered_service")

            service = Service(
                server_id="id1",
                display_name="Service 1",
                description="Description 1",
                endpoint=None,
                authentication=None,
                discovery=None,
                status="ACTIVE",
                active_revision_id="rev1",
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z"
            )
            return service
        
    def add_registered_service(self, payload: ServiceRequest) -> Service:
        with tracer.start_as_current_span("usecase.add_registered_service") as span:
            logger.info("Executing add_registered_service")
                       
            service = Service(
                server_id=payload.server_id,
                display_name=payload.display_name,
                description=payload.description,
                endpoint=payload.endpoint.__dict__ if payload.endpoint else None,
                authentication=payload.authentication.__dict__ if payload.authentication else None,
                discovery=payload.discovery.__dict__ if payload.discovery else None,
                status=payload.status,
                active_revision_id=payload.active_revision_id,
                created_at=payload.created_at,
                updated_at=payload.updated_at,
            )
            return service