from ..domain.ports import (
    IInstitutionsReader,
    IInstitutionsWriter,
    IRepresentativeReader,
    IRepresentativeWriter,
)
from .repositories import InstitutionRepository, RepresentativeRepository


def register_institutions(reg: dict):
    # Educational institution
    reg[IInstitutionsReader] = InstitutionRepository
    reg[IInstitutionsWriter] = InstitutionRepository
    # Representative
    reg[IRepresentativeWriter] = RepresentativeRepository
    reg[IRepresentativeReader] = RepresentativeRepository
