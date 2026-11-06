from mcp_gateway.domain.model.health import Health

class HealthUseCase:
    def execute(self) -> Health:
        return Health(message="true")