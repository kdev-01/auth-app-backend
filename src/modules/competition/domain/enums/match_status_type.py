from enum import Enum


class MatchStatusType(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    POSTPONED = "postponed"
    CANCELED = "canceled"
    FORFEIT = "forfeit"
