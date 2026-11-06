# Define environment variables

export VERSION=1.0
export ACCOUNT=local:localhost
export APP_NAME=py-mcp-gateway-v2
export HOST=127.0.0.1
export PORT=7499
export SESSION_TIMEOUT=700

export INVENTORY_URL=http://localhost:7000

export METRICS_HOST=127.0.0.1
export METRICS_PORT=8499

export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASS=postgres
export DB_SCHEMA=public
export DB_MAX_CONNECTION=10
export DB_SSLMODE=disable

export AUTHORIZATION_DRY_RUN=True
export AUTHORIZATION_JWKS_URL=http://localhost:7100/v1/.well-known/jwks.json
export AUTHORIZATION_ISSUER=go-authorizer-v2
export AUTHORIZATION_AUDIENCE=py-mcp-gateway-v2

export ENABLE_DNS_REBINDING_PROTECTION=False
export ALLOWED_HOSTS=localhost:*,127.0.0.1:*,py-mcp-inventory-v2:*
export ALLOWED_ORIGINS=http://localhost:*,http://127.0.0.1:*,http://py-mcp-inventory-v2:*

export MCP_PROTECTED_RESOURCE=http://localhost:7499
export AUTHORIZATION_SERVER=http://localhost:7100

export LOG_LEVEL=INFO
export OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4317
export OTEL_STDOUT_LOG_GROUP=False
export LOG_GROUP=/mnt/c/Eliezer/log/py-mcp-gateway-v2.log

# Default target
all: env activate run

PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
APP_DIR := $(PROJECT_DIR)/src

# Show environment variables
env:
	@echo "Current Environment Variables:"
	@echo "VERSION=$(VERSION)"
	@echo "ACCOUNT=$(ACCOUNT)"
	@echo "APP_NAME=$(APP_NAME)"
	@echo "HOST=$(HOST)"
	@echo "PORT=$(PORT)"
	@echo "SESSION_TIMEOUT=$(SESSION_TIMEOUT)"	
	@echo "LOG_LEVEL=$(LOG_LEVEL)"
	@echo "AUTHORIZATION_DRY_RUN=$(AUTHORIZATION_DRY_RUN)"
	@echo "AUTHORIZATION_JWKS_URL=$(AUTHORIZATION_JWKS_URL)"
	@echo "AUTHORIZATION_ISSUER=$(AUTHORIZATION_ISSUER)"
	@echo "AUTHORIZATION_AUDIENCE=$(AUTHORIZATION_AUDIENCE)"
	@echo "INVENTORY_URL=$(INVENTORY_URL)"
	@echo "METRICS_HOST=$(METRICS_HOST)"
	@echo "METRICS_PORT=$(METRICS_PORT)"
	@echo "ENABLE_DNS_REBINDING_PROTECTION=$(ENABLE_DNS_REBINDING_PROTECTION)"
	@echo "ALLOWED_HOSTS=$(ALLOWED_HOSTS)"
	@echo "ALLOWED_ORIGINS=$(ALLOWED_ORIGINS)"
	@echo "MCP_PROTECTED_RESOURCE=$(MCP_PROTECTED_RESOURCE)"
	@echo "AUTHORIZATION_SERVER=$(AUTHORIZATION_SERVER)"
	@echo "LOG_GROUP=$(LOG_GROUP)"
	@echo "OTEL_EXPORTER_OTLP_ENDPOINT=$(OTEL_EXPORTER_OTLP_ENDPOINT)"
	@echo "OTEL_STDOUT_LOG_GROUP=$(OTEL_STDOUT_LOG_GROUP)"
activate:
	@echo "Activate venv..."
	@bash -c "source ../../.venv/bin/activate"

# Run the Python application
run:
	@echo "Running application with environment variables..."
	@bash -lc "if [ -f ../../.venv/bin/activate ]; then source ../../.venv/bin/activate; fi; PYTHONPATH='$(APP_DIR)' python -m mcp_gateway.main"
    
.PHONY: all env activate run