from enum import Enum


class EventStatusType(Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELED = "canceled"
    POSTPONED = "postponed"
