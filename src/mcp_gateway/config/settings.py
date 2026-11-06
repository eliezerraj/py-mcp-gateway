import os

class Settings:
    def __init__(self):
        self.VERSION = os.getenv("VERSION")
        self.ACCOUNT = os.getenv("ACCOUNT")
        self.APP_NAME = os.getenv("APP_NAME")
        self.HOST = os.getenv("HOST")
        self.PORT = os.getenv("PORT")
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT"))
     
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_SCHEMA = os.getenv("DB_SCHEMA")
        self.DB_MAX_CONNECTION = os.getenv("DB_MAX_CONNECTION")
        self.DB_SSLMODE = os.getenv("DB_SSLMODE")     
     
        self.AUTHORIZATION_DRY_RUN = os.getenv("AUTHORIZATION_DRY_RUN", "true").lower() == "true"
        self.AUTHORIZATION_JWKS_URL = os.getenv("AUTHORIZATION_JWKS_URL")
        self.AUTHORIZATION_ISSUER = os.getenv("AUTHORIZATION_ISSUER")
        self.AUTHORIZATION_AUDIENCE = os.getenv("AUTHORIZATION_AUDIENCE")
        
        self.ENABLE_DNS_REBINDING_PROTECTION = os.getenv("ENABLE_DNS_REBINDING_PROTECTION", "false").lower() == "true"
        self.ALLOWED_HOSTS = [
            host.strip()
            for host in os.getenv("ALLOWED_HOSTS").split(",")
            if host.strip()
        ]
        self.ALLOWED_ORIGINS = [
            origin.strip()
            for origin in os.getenv("ALLOWED_ORIGINS").split(",")
            if origin.strip()
        ]
        
        self.MCP_PROTECTED_RESOURCE = os.getenv("MCP_PROTECTED_RESOURCE")
        self.AUTHORIZATION_SERVER = os.getenv("AUTHORIZATION_SERVER")

        self.METRICS_HOST = os.getenv("METRICS_HOST")
        self.METRICS_PORT = int(os.getenv("METRICS_PORT", 8601))
                    
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        self.OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        self.OTEL_STDOUT_LOG_GROUP = os.getenv("OTEL_STDOUT_LOG_GROUP", "false").lower() == "true"
        self.LOG_GROUP = os.getenv("LOG_GROUP")

settings = Settings()