
from pydantic import BaseModel
from datetime import datetime

from .user import User
from .activities import ActivityTaskDataResponse


class ProofResponse(BaseModel):
    id: int
    photo_ids: list[int]
    caption: str
    sent_on: datetime

    class Config:
        orm_mode = True


class ProofLoadedReasonse(ProofResponse):
    user: User
    task: ActivityTaskDataResponse

    class Config:
        orm_mode = True


class ProofCreate(BaseModel):
    user_id: int
    task_id: int
    photo_ids: list[int] | None
    caption: str
