import logging

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

            service = Service(id="id1", name="Service 1")
            return service
        
    def add_registered_service(self) -> Service:
        with tracer.start_as_current_span("usecase.add_registered_service") as span:
            logger.info("Executing add_registered_service")
            
            service = Service(id="id2", name="Service 2")
            return service