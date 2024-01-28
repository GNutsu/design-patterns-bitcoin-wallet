from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    api_key: str
