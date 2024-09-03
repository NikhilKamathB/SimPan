from pydantic import BaseModel


class ChatAPIResponse(BaseModel):
    success: bool
    message: str
    description: str