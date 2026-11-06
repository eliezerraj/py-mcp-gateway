# py-mcp-gateway
go-mcp-gateway

## MCP Server Registry Repository

Repository layer for `mcp_server_registry` is implemented with:

- Domain contract: `McpServerRepository`
- PostgreSQL implementation: `PostgresMcpServerRepository`
- Database access: `asyncpg` pool + parameterized raw SQL
- Coverage for create/get/list/update/delete and exception mapping in integration tests
