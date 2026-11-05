# Architecture

This document describes the high level topology, architecture system design, data flow and components relantionshios.

## Topology Overview
```mermaid
flowchart LR
    A1["Agent 1"] --> GW["MCP gateway"]
    A2["Agent 2"] --> GW
    A3["Agent 3"] --> GW

    GW --> S1["MCP server 1"]
    GW --> S2["MCP server 2"]
    GW --> S3["MCP server 3"]
```

## Architecture design Overview
```mermaid
sequenceDiagram
    participant Client as Agent MCP Client
    participant Gateway as MCP Gateway
    participant CedarPolicy as Policy Engine
    participant Catalog as Catalog Database

    Client->>Gateway: Get registered servers
    Gateway->>CedarPolicy: Evaluate workload authorization
    CedarPolicy-->>Gateway: Authorized
    Gateway->>Catalog: Read active MCP/a2a revisions
    Catalog-->>Gateway: Server and capability metadata
    Gateway-->>Client: Filtered server catalog
    Client->>Gateway: Get tools/list
    Gateway->>Catalog: Read registered tools
    Catalog-->>Gateway: Registered tools
    Gateway-->>Client: Authorized tools

    Client->>Gateway: Get resources/list
    Gateway->>Catalog: Read registered resources
    Catalog-->>Gateway: Registered resources
    Gateway-->>Client: Authorized resources

    Client->>Gateway: Get prompts/list
    Gateway->>Catalog: Read registered prompts
    Catalog-->>Gateway: Registered prompts
    Gateway-->>Client: Authorized prompts
```

## Components