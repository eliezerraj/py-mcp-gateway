from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

class ServiceEndpoint(BaseModel):
    url: str
    transport: str

class ServiceAuthentication(BaseModel):
    type: str
    audience: str
    
class ServiceDiscovery(BaseModel):
    enabled: bool = Field(default=True)
    refresh_interval_seconds: int = Field(default=0)
    
class Service(BaseModel):
    server_id: str
    name: str
    description: str
    endpoint: Optional[ServiceEndpoint]
    authentication: Optional[ServiceAuthentication]
    discovery: Optional[ServiceDiscovery]
    status: str
    active_revision_id: str
    created_at: Optional[str]
    updated_at: Optional[str]