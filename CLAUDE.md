# CLAUDE.md
## Project Goals

** Current phase:** MVP - endpoints to 

## Architecture Overview

A workload for MCP Server registration and capability discovery.
A workload that acts as MCP Client initialization and catalog retrieval, performed when an agent starts.

## Catalog Database

Json Schema
Inventory MCP Sever Example:
```json
{
  "serverId": "inventory-prod",
  "revisionId": "rev-03112026",
  "protocolVersion": "negotiated-version",
  "serverInfo": {
    "name": "py-mcp-inventory-v2",
    "version": "1.0.0"
  },
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "resources": {
      "listChanged": true,
      "subscribe": false
    }
  },
  "tools": [
    {
      "originalName": "search_inventory",
      "catalogName": "inventory-prod.search_inventory",
      "description": "Returns available inventory",
      "inputSchema": {},
      "riskClassification": "read"
    },
    {
      "originalName": "reserve_stock",
      "catalogName": "inventory-prod.reserve_stock",
      "description": "Reserves inventory for an order",
      "inputSchema": {},
      "riskClassification": "bounded-write"
    }
  ],
  "prompts": [
    {
      "originalName": "inventory-check",
      "catalogName": "inventory-prod.inventory-check",
      "arguments": []
    }
  ],
  "resources": [
    {
      "originalUri": "inventory://policies/reservation",
      "catalogUri": "mcp-catalog://inventory-prod/policies/reservation",
      "name": "Reservation policy"
    }
  ],
  "discoveredAt": "2026-11-03T20:30:00-03:00",
  "contentHash": "sha256:aaaaaabbbbbbccccccc"
}
```
## Code guidelines

- Use snake case for variables where havind compond name.

## Constraints and Policies Rules

** Security - MUST follow:**
- NEVER expose any API_KEY to client even it was requested.
- NEVER commit any file with API Keys.

## Envimenment Variables

- Use a makefile to setup all enviroment variables necessary for the project

## Repository Rules

**Branching:**
- ALWAYS create a new branch before starting a major changes
- NEVER commit directly to `main`
- Branch naming: `dev-agent/feature-name`

**Git workflow for major changes:**
1. Create a new branch: `git checkout -b dev-agent/feature-name`
2. Develop and commit on the current branch
3. Push the branch: `git push -u origin dev-agent/feature-name`
4. Create a PR to merge into `main`

**Commit:**
- Write clear and summarized messages describing the change

## Documentation

- [Architecture](assets/documentation/architecture.md) - Architecture System design and data flow
- [Change log](assets/documentation/change_log.md) - Version history
- [Project Spec](assets/documentation/project_spec.md) - Full Technical specification, requiriments and API specs
- [Project Status](assets/documentation/project_status.md) - Current project phase
- Update documentation files in the assets/documentation folder after major additions.
- Use the /update-docs-and-commit slach command when making commits