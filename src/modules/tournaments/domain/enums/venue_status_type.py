from enum import Enum


class VenueStatusType(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_USE = "in_use"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"
