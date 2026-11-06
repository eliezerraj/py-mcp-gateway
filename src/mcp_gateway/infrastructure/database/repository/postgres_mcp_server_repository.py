from __future__ import annotations

from datetime import timezone

import asyncpg

from mcp_gateway.domain.exceptions import (
    McpServerAlreadyExistsError,
    McpServerNotFoundError,
    RepositoryError,
)
from mcp_gateway.domain.model.service import Service
from mcp_gateway.domain.repository.mcp_server_repository import McpServerRepository


class PostgresMcpServerRepository(McpServerRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, service: Service) -> Service:
        server_id = self._resolve_server_id(service)
        endpoint_url = self._resolve_endpoint_url(service)

        try:
            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    INSERT INTO mcp_server_registry (
                        server_id,
                        endpoint_url,
                        status,
                        document,
                        discovered_at,
                        content_hash
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING
                        server_id,
                        endpoint_url,
                        status,
                        document,
                        discovered_at,
                        content_hash,
                        created_at,
                        updated_at
                    """,
                    server_id,
                    endpoint_url,
                    service.status.value,
                    service.document,
                    service.discovered_at,
                    service.content_hash,
                )
        except asyncpg.UniqueViolationError as exc:
            raise McpServerAlreadyExistsError(
                f"mcp server '{server_id}' already exists"
            ) from exc
        except asyncpg.PostgresError as exc:
            raise RepositoryError("failed to create mcp server") from exc

        return self._to_domain(row)

    async def get_by_id(self, server_id: str) -> Service | None:
        try:
            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    SELECT
                        server_id,
                        endpoint_url,
                        status,
                        document,
                        discovered_at,
                        content_hash,
                        created_at,
                        updated_at
                    FROM mcp_server_registry
                    WHERE server_id = $1
                    """,
                    server_id,
                )
        except asyncpg.PostgresError as exc:
            raise RepositoryError("failed to get mcp server by id") from exc

        if row is None:
            return None

        return self._to_domain(row)

    async def list(
        self,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Service]:
        effective_limit = min(limit, 100)

        try:
            async with self._pool.acquire() as connection:
                if status is None:
                    rows = await connection.fetch(
                        """
                        SELECT
                            server_id,
                            endpoint_url,
                            status,
                            document,
                            discovered_at,
                            content_hash,
                            created_at,
                            updated_at
                        FROM mcp_server_registry
                        ORDER BY created_at DESC
                        LIMIT $1
                        OFFSET $2
                        """,
                        effective_limit,
                        offset,
                    )
                else:
                    rows = await connection.fetch(
                        """
                        SELECT
                            server_id,
                            endpoint_url,
                            status,
                            document,
                            discovered_at,
                            content_hash,
                            created_at,
                            updated_at
                        FROM mcp_server_registry
                        WHERE status = $1
                        ORDER BY created_at DESC
                        LIMIT $2
                        OFFSET $3
                        """,
                        status,
                        effective_limit,
                        offset,
                    )
        except asyncpg.PostgresError as exc:
            raise RepositoryError("failed to list mcp servers") from exc

        return [self._to_domain(row) for row in rows]

    async def update(self, service: Service) -> Service:
        server_id = self._resolve_server_id(service)
        endpoint_url = self._resolve_endpoint_url(service)

        try:
            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    UPDATE mcp_server_registry
                    SET
                        endpoint_url = $2,
                        status = $3,
                        document = $4,
                        discovered_at = $5,
                        content_hash = $6,
                        updated_at = NOW()
                    WHERE server_id = $1
                    RETURNING
                        server_id,
                        endpoint_url,
                        status,
                        document,
                        discovered_at,
                        content_hash,
                        created_at,
                        updated_at
                    """,
                    server_id,
                    endpoint_url,
                    service.status,
                    service.document,
                    service.discovered_at,
                    service.content_hash,
                )
        except asyncpg.PostgresError as exc:
            raise RepositoryError("failed to update mcp server") from exc

        if row is None:
            raise McpServerNotFoundError(f"mcp server '{server_id}' not found")

        return self._to_domain(row)

    async def delete(self, server_id: str) -> bool:
        try:
            async with self._pool.acquire() as connection:
                result = await connection.execute(
                    """
                    DELETE FROM mcp_server_registry
                    WHERE server_id = $1
                    """,
                    server_id,
                )
        except asyncpg.PostgresError as exc:
            raise RepositoryError("failed to delete mcp server") from exc

        return result == "DELETE 1"

    @staticmethod
    def _resolve_server_id(service: McpServer) -> str:
        if service.server_id:
            return service.server_id
        value = service.document.get("serverId")
        if isinstance(value, str) and value:
            return value
        raise RepositoryError("service.server_id is required")

    @staticmethod
    def _resolve_endpoint_url(service: McpServer) -> str:
        if service.endpoint_url:
            return service.endpoint_url

        endpoint = service.document.get("endpoint")
        if isinstance(endpoint, dict):
            value = endpoint.get("url")
            if isinstance(value, str) and value:
                return value

        raise RepositoryError("service.endpoint_url is required")

    @staticmethod
    def _to_domain(row: asyncpg.Record) -> Service:
        created_at = row["created_at"]
        updated_at = row["updated_at"]
        discovered_at = row["discovered_at"]

        if created_at is not None and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if updated_at is not None and updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        if discovered_at is not None and discovered_at.tzinfo is None:
            discovered_at = discovered_at.replace(tzinfo=timezone.utc)

        return Service(
            server_id=row["server_id"],
            endpoint_url=row["endpoint_url"],
            status=row["status"],
            document=dict(row["document"]),
            discovered_at=discovered_at,
            content_hash=row["content_hash"],
            created_at=created_at,
            updated_at=updated_at,
        )
