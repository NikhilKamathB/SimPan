from pydantic import BaseModel
from typing import List, Union


class BaseErrorStruct(BaseModel):
    code: int
    message: str


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Union[dict, List[dict]] = None