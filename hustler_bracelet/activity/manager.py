# -*- coding: utf-8 -*-

from hustler_bracelet.database.activity import Activity
from .activity_task import ActivityTask
from .niche import Niche
from datetime import datetime
from hustler_bracelet.utils import create_int_uid


class ActivityManager:
    def __init__(self):
        pass  # TODO

    async def begin_activity(
            self,
            name: str,
            description: str,
            deadline: datetime,
            fund: int,
            places: int,
            niches: list[Niche],
            tasks: list[ActivityTask]
    ) -> Activity:
        activity = Activity(
            id=create_int_uid(),
            name=name,
            description=description,
            # TODO
        )
        return activity
