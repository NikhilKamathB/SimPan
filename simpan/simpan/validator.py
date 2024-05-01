from typing import Optional
from pydantic import BaseModel
from workers.validators import Status


class ResponseValidator(BaseModel):

    status: Status = Status.OK
    message: Optional[str] = None
    body: Optional[dict] = None