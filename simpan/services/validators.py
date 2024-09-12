from pydantic import BaseModel
from typing import List, Optional


class BaseErrorStruct(BaseModel):
    code: int
    message: str


class BaseFileStruct(BaseModel):
    id: str
    name: str
    url: str
    type: str


class ChatResponse(BaseModel):
    chatResponse: str
    files: Optional[List[BaseFileStruct]] = None


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict = None