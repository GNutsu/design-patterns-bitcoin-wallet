from fastapi import APIRouter, status

from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable
from bitcoinwallet.infra.fastapi.model import CreateUserResponse

bitcoin_api = APIRouter(tags=["Bitcoin"])


@bitcoin_api.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
def create_user(bitcoin_service: BitcoinServiceDependable) -> CreateUserResponse:
    api_key = bitcoin_service.create_user()
    return CreateUserResponse(api_key=api_key)
