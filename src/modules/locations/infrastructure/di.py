from ..domain.ports import ICityReader
from .repositories.city_repository import CityRepository


def register_cities(reg: dict):
    reg[ICityReader] = CityRepository
    