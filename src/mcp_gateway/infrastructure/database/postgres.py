from __future__ import annotations

import asyncpg

async def create_postgres_pool(
    dsn: str,
    *,
    min_size: int = 1,
    max_size: int = 10,
) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=min_size,
        max_size=max_size,
    )

async def close_postgres_pool(pool: asyncpg.Pool | None) -> None:
    if pool is not None:
        await pool.close()
