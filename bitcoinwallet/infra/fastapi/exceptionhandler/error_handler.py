from typing import cast

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from bitcoinwallet.core.model.exception.exception import (
    ForbiddenException,
    NotFoundException,
)


def not_found_exception_handler(request: Request, exc: Exception) -> Response:
    not_found_exception = cast(NotFoundException, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": not_found_exception.get_msg()}},
    )


def forbidden_exception_handler(request: Request, exc: Exception) -> Response:
    forbidden_exception = cast(ForbiddenException, exc)
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": {"message": forbidden_exception.get_msg()}},
    )
