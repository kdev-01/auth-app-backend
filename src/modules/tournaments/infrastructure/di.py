from ..domain.ports import IAcademicYearReader
from .repositories import AcademicYearRepository


def register_tournaments(reg: dict):
    # Academic year
    reg[IAcademicYearReader] = AcademicYearRepository
