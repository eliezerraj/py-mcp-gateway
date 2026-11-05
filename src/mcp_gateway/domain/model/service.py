from pydantic import BaseModel, Field

# Domain model for a service
class Service(BaseModel):
    id: str = Field(default=None, description="The unique identifier of the service")
    name: str = Field(default=None, description="The name of the service")