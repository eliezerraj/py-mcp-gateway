project:
  name: mcp-gateway
  language: Python
  python_version: "3.14"
  framework: FastAPI
  architecture: Clean Architecture

objective:
  description: >
    Implement the repository layer for CRUD operations on the
    mcp_server_registry PostgreSQL table.
  scope: repository-layer-only
  existing_scaffold: true

constraints:
  - Do not modify controllers, routes, middleware, or use cases unless required for imports.
  - Do not implement business logic inside the repository.
  - Do not return Request DTOs or Response DTOs from the repository.
  - Do not use an ORM.
  - Do not use SQLAlchemy.
  - Use raw SQL.
  - Use asyncpg as the PostgreSQL driver.
  - Use asynchronous database operations.
  - Always use parameterized SQL queries.
  - Never construct SQL using string interpolation with user-provided values.
  - Do not create database tables at application startup.
  - Do not silently catch database exceptions.
  - Preserve the JSON document as PostgreSQL JSONB.

technology:
  database: PostgreSQL
  database_driver: asyncpg
  database_access: raw_sql
  orm: none
  migration_tool: Alembic

project_structure:
  domain:
    repository_interface: src/mcp_gateway/domain/repository/mcp_server_repository.py
    model: src/mcp_gateway/domain/model/service.py

  infrastructure:
    database_pool: src/mcp_gateway/infrastructure/database/postgres.py
    repository_implementation: src/mcp_gateway/infrastructure/database/repository/postgres_mcp_server_repository.py

  bootstrap:
    dependency_container: src/mcp_gateway/bootstrap/container.py

database:
  table: mcp_server_registry

  schema: |
    CREATE TABLE mcp_server_registry (
        server_id VARCHAR(100) PRIMARY KEY,
        endpoint TEXT NOT NULL,
        status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',

        document JSONB NOT NULL,

        discovered_at TIMESTAMPTZ,
        content_hash VARCHAR(100),

        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        CONSTRAINT ck_mcp_server_status
            CHECK (status IN ('ACTIVE', 'INACTIVE', 'UNHEALTHY')),

        CONSTRAINT ck_mcp_server_document
            CHECK (jsonb_typeof(document) = 'object')
    );

repository_contract:
  interface_name: McpServerRepository
  implementation_name: PostgresMcpServerRepository

  methods:

    create:
      signature: >
        async def create(
            self,
            service: McpServer
        ) -> McpServer
      behavior:
        - Insert a new registry record.
        - Save the complete service document as JSONB.
        - Copy service.endpoint.url into endpoint.
        - Use PostgreSQL RETURNING to retrieve the inserted record.
        - Convert the database row into a domain model.
        - Raise McpServerAlreadyExistsError when server_id already exists.

    get_by_id:
      signature: >
        async def get_by_id(
            self,
            server_id: str
        ) -> McpServer | None
      behavior:
        - Execute a SELECT using server_id.
        - Return the corresponding domain model.
        - Return None when the record does not exist.

    list:
      signature: >
        async def list(
            self,
            status: McpServerStatus | None = None,
            limit: int = 100,
            offset: int = 0
        ) -> list[McpServer]
      behavior:
        - Return records ordered by created_at DESC.
        - Filter by status when provided.
        - Use parameterized LIMIT and OFFSET.
        - Enforce a maximum limit of 100.

    update:
      signature: >
        async def update(
            self,
            service: McpServer
        ) -> McpServer
      behavior:
        - Update endpoint.
        - Update status.
        - Update document.
        - Update discovered_at when applicable.
        - Update content_hash when applicable.
        - Set updated_at = NOW().
        - Never modify created_at.
        - Use RETURNING to retrieve the updated row.
        - Raise McpServerNotFoundError when no row is updated.

    delete:
      signature: >
        async def delete(
            self,
            server_id: str
        ) -> bool
      behavior:
        - Delete the record using server_id.
        - Return true when one record is deleted.
        - Return false when no record exists.

sql_requirements:
  parameter_style: asyncpg

  example:
    incorrect: |
      query = f"SELECT * FROM mcp_server_registry WHERE server_id = '{server_id}'"

    correct: |
      query = """
      SELECT *
      FROM mcp_server_registry
      WHERE server_id = $1
      """

      row = await connection.fetchrow(query, server_id)

connection_management:
  type: asyncpg_pool

  startup:
    - Create one asyncpg connection pool for the application.

  repository:
    - Inject the asyncpg pool into the repository constructor.
    - Acquire connections from the pool.
    - Release connections automatically using async context managers.
    - Do not create a new database connection for each repository instance.

  example: |
    class PostgresMcpServerRepository:

        def __init__(self, pool: asyncpg.Pool):
            self._pool = pool

        async def get_by_id(
            self,
            server_id: str,
        ) -> McpServer | None:

            async with self._pool.acquire() as connection:
                row = await connection.fetchrow(
                    """
                    SELECT *
                    FROM mcp_server_registry
                    WHERE server_id = $1
                    """,
                    server_id,
                )

            if row is None:
                return None

            return self._to_domain(row)

transaction_policy:
  default:
    - A single INSERT, UPDATE, or DELETE statement is atomic in PostgreSQL.
    - Do not manually commit individual statements.

  multi_statement_operations:
    - Use asyncpg transactions when an operation contains multiple dependent SQL statements.

  example: |
    async with self._pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(...)
            await connection.execute(...)

domain_mapping:
  domain_model: McpServer

  rules:
    - serverId maps to server_id.
    - endpoint.url maps to endpoint.
    - status maps to status.
    - The complete service payload maps to document.
    - Database timestamps must be timezone-aware.
    - The domain layer must not import asyncpg.
    - The domain layer must not contain database-specific code.
    - Mapping between asyncpg.Record and the domain model must be explicit.

jsonb:
  requirements:
    - Store document using PostgreSQL JSONB.
    - Do not manually escape JSON.
    - Do not store JSON as a TEXT database column.
    - Repository is responsible for converting the domain representation into a JSON-compatible value.
    - Repository is responsible for converting the returned JSONB document back into the domain model.

exceptions:
  definitions:

    - name: McpServerAlreadyExistsError
      condition: Duplicate server_id

    - name: McpServerNotFoundError
      condition: Update target does not exist

    - name: RepositoryError
      condition: Unexpected database error

  mapping:
    asyncpg.UniqueViolationError: McpServerAlreadyExistsError
    asyncpg.PostgresError: RepositoryError

  requirements:
    - Database exceptions must not escape into the domain or use-case layer.
    - Preserve original exceptions using Python exception chaining.

payload_example:
  serverId: inventory-prod
  displayName: Production Inventory MCP Server
  description: Inventory lookup and reservation capabilities
  environment: prod

  endpoint:
    url: https://inventory-mcp.internal.example.com/mcp
    transport: streamable-http

  authentication:
    type: oauth2
    audience: mcp-inventory

  owner:
    team: inventory-platform

  discovery:
    enabled: true
    refreshIntervalSeconds: 900

  status: ACTIVE
  activeRevisionId: rev-84f216
  createdAt: "2026-11-03T20:20:00-03:00"
  updatedAt: "2026-11-03T20:30:00-03:00"

acceptance_criteria:
  - Repository interface exists in the domain layer.
  - PostgreSQL repository implementation exists in the infrastructure layer.
  - No ORM is used.
  - SQLAlchemy is not installed or imported for repository functionality.
  - All database operations use asyncpg.
  - All SQL statements are parameterized.
  - Repository receives asyncpg.Pool through constructor injection.
  - JSON payload is persisted as PostgreSQL JSONB.
  - Repository returns domain models only.
  - INSERT and UPDATE use RETURNING where appropriate.
  - Duplicate server IDs produce McpServerAlreadyExistsError.
  - Updating a missing server produces McpServerNotFoundError.
  - Integration tests cover create, get, list, update, delete, duplicate create, and missing update.

out_of_scope:
  - FastAPI route implementation
  - Request DTO implementation
  - Response DTO implementation
  - Authentication middleware
  - Authorization policies
  - Metrics
  - Tracing
  - Health endpoints
  - Registry discovery calls