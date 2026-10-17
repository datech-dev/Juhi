from typing import Any

from fastapi import HTTPException, status


class JuhiAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Any | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": error_code,
                    "message": message,
                    "details": details or {},
                }
            },
        )
        self.error_code = error_code
        self.message = message
        self.details = details


class UnauthorizedException(JuhiAPIException):
    def __init__(self, message: str = "Authentication token is invalid or expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenException(JuhiAPIException):
    def __init__(self, message: str = "Access denied for this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class NotFoundException(JuhiAPIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=message,
        )


class ConflictException(JuhiAPIException):
    def __init__(self, message: str = "Conflict with existing state or idempotency conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            message=message,
        )


class RateLimitExceededException(JuhiAPIException):
    def __init__(self, message: str = "Too many requests. Please slow down."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            message=message,
        )
