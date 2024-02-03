from fastapi import Request, status
from fastapi.responses import JSONResponse

from bitcoinwallet.core.service.exception import ForbiddenException, NotFoundException


def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.get_msg()}},
    )


def forbidden_exception_handler(
    request: Request, exc: ForbiddenException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": {"message": exc.get_msg()}},
    )
