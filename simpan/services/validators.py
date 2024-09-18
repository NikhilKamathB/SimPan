from pydantic import BaseModel
from typing import List, Optional, Union


class BaseErrorStruct(BaseModel):
    code: int
    message: str


class BaseFileStruct(BaseModel):
    id: str
    name: str
    url: str
    type: str


class ChatResponse(BaseModel):
    workspace_id: str
    chat_response: str
    files: Optional[List[BaseFileStruct]] = None


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Union[dict, List[dict]] = None