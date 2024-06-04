# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ActivityTask:
    name: str
    description: str
    deadline: datetime
    points: int
