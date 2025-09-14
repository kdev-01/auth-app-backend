from src.core.responses.custom_exceptions import BadRequest, NotFound

from ...domain.ports import IInstitutionsReader, IInstitutionsWriter


class InstitutionDelete():
    def __init__(
        self,
        reader: IInstitutionsReader,
        writer: IInstitutionsWriter,
    ):
        self.reader = reader
        self.writer = writer
        
    async def delete(self, target_id: int) -> None:
        institution = await self.reader.get_by_id(target_id)
        if not institution:
            raise NotFound(
                message="El institution no existe.",
                code="INSTITUTION_NOT_FOUND"
            )
        
        ok = await self.writer.soft_delete(target_id)
        if not ok:
            raise BadRequest(
                message="No se pudo eliminar a la institución educativa."
            )
    