from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any


def http_error_response(status_code: int, code: str, message: str, details: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details}},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Mapping status codes to readable codes
    status_mapping = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "unprocessable_entity",
        500: "internal_server_error",
    }
    code = status_mapping.get(exc.status_code, f"error_{exc.status_code}")
    message = exc.detail if isinstance(exc.detail, str) else "An error occurred"
    return http_error_response(status_code=exc.status_code, code=code, message=message)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return http_error_response(
        status_code=422,
        code="validation_error",
        message="Invalid request parameters",
        details=exc.errors(),
    )


async def general_exception_handler(request: Request, exc: Exception):
    return http_error_response(
        status_code=500,
        code="internal_server_error",
        message="An unexpected error occurred",
    )
