from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from bitcoinwallet.core.model.exception import ForbiddenException, NotFoundException


def not_found_exception_handler(request: Request, exc: NotFoundException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.get_msg()}},
    )


def forbidden_exception_handler(request: Request, exc: ForbiddenException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": {"message": exc.get_msg()}},
    )
