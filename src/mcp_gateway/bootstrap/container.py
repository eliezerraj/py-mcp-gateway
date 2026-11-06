from __future__ import annotations

from dataclasses import dataclass

import asyncpg

from mcp_gateway.domain.repository.mcp_server_repository import McpServerRepository
from mcp_gateway.infrastructure.database.postgres import (
    close_postgres_pool,
    create_postgres_pool,
)
from mcp_gateway.infrastructure.database.repository.postgres_mcp_server_repository import (
    PostgresMcpServerRepository,
)

@dataclass
class Container:
    pool: asyncpg.Pool
    mcp_server_repository: McpServerRepository

async def create_container(
    dsn: str,
    *,
    min_pool_size: int = 1,
    max_pool_size: int = 10,
) -> Container:
    pool = await create_postgres_pool(
        dsn,
        min_size=min_pool_size,
        max_size=max_pool_size,
    )
    return Container(
        pool=pool,
        mcp_server_repository=PostgresMcpServerRepository(pool),
    )

async def shutdown_container(container: Container) -> None:
    await close_postgres_pool(container.pool)
