from uuid import UUID

from src.core.responses.custom_exceptions import BadRequest, NotFound
from src.modules.institutions.domain.ports import IRepresentativeWriter

from ...domain.ports import IUserReader, IUserWriter

ROLE_REPRESENTATIVE = "Representante educativo"

class UserDelete:
    def __init__(
        self,
        reader: IUserReader,
        writer: IUserWriter,
        representative_writer: IRepresentativeWriter,
    ):
        self.reader = reader
        self.writer = writer
        self.representative_writer = representative_writer
        
    async def delete(self, target_id: UUID, requester_id: UUID, requester_role: str) -> None:
        if target_id == requester_id:
            raise BadRequest("No puedes eliminarte a ti mismo.")
        
        user = await self.reader.get_by_id(target_id)
        if not user:
            raise NotFound(
                message="El usuario no existe.",
                code="USER_NOT_FOUND"
            )
        
        if requester_role == ROLE_REPRESENTATIVE:
            ok_rep = await self.representative_writer.unassign_active(target_id)
            if not ok_rep:
                raise BadRequest("No se pudo eliminar el usuario.")
        
        ok = await self.writer.soft_delete(target_id)
        if not ok:
             raise BadRequest(
                message="No se pudo eliminar el usuario."
            )
        