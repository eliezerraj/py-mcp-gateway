from mcp_gateway.domain.model.health import Health

from opentelemetry import trace

class HealthUseCase:
    def execute(self) -> Health:
        return Health(message="true")