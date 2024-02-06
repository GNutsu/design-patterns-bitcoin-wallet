from typing import cast

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from bitcoinwallet.core.model.exception.exception import (
    ForbiddenException,
    InvalidInputException,
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


def invalid_input_exception_handler(request: Request, exc: Exception) -> Response:
    invalid_input_exception = cast(InvalidInputException, exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"message": invalid_input_exception.get_msg()}},
    )
