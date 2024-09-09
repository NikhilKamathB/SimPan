from pydantic import BaseModel


class BaseError(BaseModel):
    code: int
    message: str


class ChatResponse(BaseModel):
    chatResponse: str


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict = None