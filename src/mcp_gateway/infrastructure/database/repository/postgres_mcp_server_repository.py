from __future__ import annotations

import logging
import json
from datetime import datetime, timezone
import json
import asyncpg

from datetime import timezone

from mcp_gateway.domain.exceptions import (
    McpServerAlreadyExistsError,
    McpServerNotFoundError,
    RepositoryError,
)
from mcp_gateway.domain.model.service import Service
from mcp_gateway.domain.repository.mcp_server_repository import McpServerRepository

from opentelemetry import trace
#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class PostgresMcpServerRepository(McpServerRepository):
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, service: Service) -> Service:
        logger.info(f"================================= Executing create registered service: {service}")
        with tracer.start_as_current_span("usecase.create_registered_service") as span:
            
            server_id = self._resolve_server_id(service)
            endpoint = self._resolve_endpoint(service)
            status_value = service.status.value if hasattr(service.status, "value") else service.status
            document = self._service_to_document(service)
            document_json = json.dumps(document)
            now = datetime.now(timezone.utc)
            
            print("-----------------------")
            print(f"server_id: {server_id}")
            print(f"endpoint: {endpoint}")
            print(f"status_value: {status_value}")
            print(f"document: {document}")
            print("-----------------------")
            
            try:
                async with self._pool.acquire() as connection:
                    row = await connection.fetchrow(
                        """
                        INSERT INTO mcp_server_registry (
                            server_id,
                            endpoint,
                            status,
                            document,
                            discovered_at,
                            content_hash
                        )
                        VALUES ($1, $2, $3, $4::jsonb, $5, $6)
                        RETURNING
                            server_id,
                            endpoint,
                            status,
                            document,
                            discovered_at,
                            content_hash,
                            created_at,
                            updated_at
                        """,
                        server_id,
                        endpoint,
                        status_value,
                        document_json,
                        now,
                        None,
                    )
            except asyncpg.UniqueViolationError as exc:
                raise McpServerAlreadyExistsError(
                    f"mcp server '{server_id}' already exists"
                ) from exc
            except asyncpg.PostgresError as exc:
                logger.error(
                    "Postgres error on create: %s | sqlstate=%s | detail=%s",
                    str(exc),
                    getattr(exc, "sqlstate", None),
                    getattr(exc, "detail", None),
                )
                raise RepositoryError(f"failed to createmcp_server_registry {str(exc)}") from exc

            return self._to_domain(row)

    async def get_by_id(self, server_id: str) -> Service | None:
        try:
            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    SELECT
                        server_id,
                        endpoint,
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
                            endpoint,
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
                            endpoint,
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
        endpoint = self._resolve_endpoint(service)
        status_value = service.status.value if hasattr(service.status, "value") else service.status
        document = self._service_to_document(service)
        document_json = json.dumps(document)
        try:
            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    UPDATE mcp_server_registry
                    SET
                        endpoint = $2,
                        status = $3,
                        document = $4::jsonb,
                        discovered_at = NOW(),
                        content_hash = $5,
                        created_at = NOW()
                    WHERE server_id = $1
                    RETURNING
                        server_id,
                        endpoint,
                        status,
                        document,
                        discovered_at,
                        content_hash,
                        created_at,
                        updated_at
                    """,
                    server_id,
                    endpoint,
                    status_value,
                    document_json,
                    None,
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
    def _resolve_server_id(service: Service) -> str:
        if service.server_id:
            return service.server_id
        raise RepositoryError("service.server_id is required")

    @staticmethod
    def _resolve_endpoint(service: Service) -> str:
        if service.endpoint:
            return service.endpoint.url

        raise RepositoryError("service.endpoint is required")

    @staticmethod
    def _service_to_document(service: Service) -> dict:
        return service.model_dump(mode="json", exclude_none=True)

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

        raw_document = row["document"]
        if isinstance(raw_document, str):
            document = json.loads(raw_document)
        elif isinstance(raw_document, dict):
            document = raw_document
        else:
            document = {}

        if "server_id" not in document:
            document["server_id"] = row["server_id"]
        if "status" not in document:
            document["status"] = row["status"]
        if "created_at" not in document and created_at is not None:
            document["created_at"] = created_at.isoformat()
        if "updated_at" not in document and updated_at is not None:
            document["updated_at"] = updated_at.isoformat()
        if "endpoint" not in document:
            document["endpoint"] = {"url": row["endpoint"], "transport": "streamable-http"}

        return Service(**document)
