from __future__ import annotations

from abc import ABC, abstractmethod

from mcp_gateway.domain.model.service import Service

class McpServerRepository(ABC):
    @abstractmethod
    async def create(self, service: Service) -> Service:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, server_id: str) -> Service | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, service: Service) -> Service:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, server_id: str) -> bool:
        raise NotImplementedError
