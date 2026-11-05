from dataclasses import dataclass
from pydantic import Field
from mcp_gateway.domain.model.service import Service

# Result for the health check
@dataclass(frozen=True)
class HealthResponse:
    message: str
    
# Result for a single service
@dataclass(frozen=True)
class ServiceResponse:
    message: str
    service: Service