from dataclasses import replace
from typing import List
from uuid import UUID

from src.modules.institutions.domain.ports import IRepresentativeReader

from ...domain.dto import InstitutionDTO, UserDTO
from ...domain.ports import IUserReader

ROLE_REPRESENTATIVE = "Representante educativo"


class UserRead:
    def __init__(
        self, reader: IUserReader, representative_reader: IRepresentativeReader
    ):
        self.reader = reader
        self.representative = representative_reader

    async def retrieve_all_users(self, exclude_user_id: UUID) -> List[UserDTO]:
        data = await self.reader.list_all(exclude_user_id)

        rep_ids = [u.person_id for u in data if u.role.name == ROLE_REPRESENTATIVE]

        assignments_list = await self.representative.get_current_assignments(rep_ids)
        assignments_by_user = {
            a.user_person_id: InstitutionDTO(
                institution_id=a.institution.institution_id, name=a.institution.name
            )
            for a in assignments_list
        }

        enriched: list[UserDTO] = []
        for u in data:
            if u.role.name == ROLE_REPRESENTATIVE:
                inst = assignments_by_user.get(u.person_id)
                if inst:
                    enriched.append(replace(u, role=replace(u.role, institution=inst)))
                    continue
            enriched.append(u)

        return enriched
