from src.mcp_gateway.domain.external.error_response import AppError

class InvalidAccessTokenError(AppError):
    pass

class AuthorizationDeniedError(AppError):
    pass

class MissingTokenError(AppError):
    pass

class ForbiddenError(AppError):
    pass

class McpServerAlreadyExistsError(Exception):
    pass

class McpServerNotFoundError(Exception):
    pass

class RepositoryError(Exception):
    pass