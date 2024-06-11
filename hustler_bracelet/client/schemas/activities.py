
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from .leaderboard import LeaderBoardItem


class ActivityTaskData(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int


class ActivityTaskCreateData(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int


class NicheData(BaseModel):
    name: str
    description: str
    task: ActivityTaskData


class ActivityDataCreate(BaseModel):
    name: str
    description: str
    fund: int
    total_places: int = Field(alias='places')
    deadline: datetime


class ActivityDataResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str
    fund: int
    total_places: int
    started_on: datetime
    deadline: datetime

    niches: list['NicheDataResponse']

    class Config:
        orm_mode = True


class NicheDataResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str

    tasks: list['ActivityTaskDataResponse']

    class Config:
        orm_mode = True


class UserNicheResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str

    task: Optional['ActivityTaskDataResponse']

    class Config:
        orm_mode = True


class ActivityTaskDataResponse(BaseModel):
    id: int
    name: str
    description: str
    points: int
    added_on: datetime
    deadline: datetime

    class Config:
        orm_mode = True


class ActivitySummaryResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str
    fund: int
    total_places: int
    started_on: datetime
    deadline: datetime

    leaderboard_data: list[LeaderBoardItem] | None
    user_leaderboard_data: LeaderBoardItem | None
    niche: UserNicheResponse

    class Config:
        orm_mode = True


class ActivityStartRequestData(BaseModel):
    activity: ActivityDataCreate
    niches: list[NicheData]


class ActivityStartResponseData(BaseModel):
    did_start_activity: bool
    description: str


class ActivityUserStatusResponse(BaseModel):
    is_running: bool
    occupied_places: int
    total_places: int
    can_join: bool
    already_joined: bool


class ActivityTaskStatus(BaseModel):
    can_do_task: bool
    already_done: bool

