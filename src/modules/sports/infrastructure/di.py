from ..domain.ports import ISportReader
from .repositories import SportRepository


def register_sports(reg: dict):
    # Sport
    reg[ISportReader] = SportRepository
