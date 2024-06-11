
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    success: bool
    message: str
