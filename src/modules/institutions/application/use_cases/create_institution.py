from src.core.responses.custom_exceptions import ConflictError

from ...domain.dto import InstitutionDTO
from ...domain.ports import IInstitutionsReader, IInstitutionsWriter


class InstitutionCreate:
    def __init__(
        self,
        reader: IInstitutionsReader,
        writer: IInstitutionsWriter
    ):
        self.reader = reader
        self.writer = writer
    
    async def create_institution(
        self,
        name: str,
        city_id: int | None = None,
    ) -> InstitutionDTO:
        if await self.reader.get_by_name(name):
            raise ConflictError(
                message="La institución educativa ya existe.",
                code="INSTITUTION_ALREADY_EXISTS"
            )
        
        created = await self.writer.create(
            name=name,
            city_id=city_id
        )
        
        return created
    