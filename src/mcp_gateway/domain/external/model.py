from dataclasses import dataclass
from pydantic import Field
from mcp_gateway.domain.model.service import Service
from typing import Optional

# Result for the health check
@dataclass(frozen=True)
class HealthResponse:
    message: str
    
# Result for a single service
@dataclass(frozen=True)
class ServiceResponse:
    message: str
    service: Service

@dataclass(frozen=True)
class ServiceEndpointRequest:
    url: str
    transport: str

@dataclass(frozen=True)
class ServiceAuthenticationRequest:
    type: str
    audience: str

@dataclass(frozen=True)
class ServiceDiscoveryRequest:
    enabled: bool = Field(default=True)
    refresh_interval_seconds: int = Field(default=0)

@dataclass(frozen=True)
class ServiceRequest:
    server_id: str
    display_name: str
    description: str
    endpoint: Optional[ServiceEndpointRequest]
    authentication: Optional[ServiceAuthenticationRequest]
    discovery: Optional[ServiceDiscoveryRequest]
    status: str
    active_revision_id: str
    created_at: Optional[str]
    updated_at: Optional[str]