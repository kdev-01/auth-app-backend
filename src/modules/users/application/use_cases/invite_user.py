from uuid import UUID

from src.core.email import EmailMessage, IEmailService, render_template
from src.core.responses.custom_exceptions import (
    BadRequest,
    ConflictError,
    EmailAlreadyExists,
)
from src.core.security.interface import IJWTService
from src.modules.institutions.domain.ports import IRepresentativeWriter

from ...domain.dto import UserDTO
from ...domain.ports import IUserReader, IUserWriter

ROLE_REPRESENTATIVE = "Representante educativo"


class InviteUser:
    def __init__(
        self,
        reader: IUserReader,
        writer: IUserWriter,
        representative_writer: IRepresentativeWriter,
        email: IEmailService,
        jwt: IJWTService,
        frontend_base_url: str,
        from_email: str,
    ):
        self.reader = reader
        self.writer = writer
        self.representative_writer = representative_writer
        self.email = email
        self.jwt = jwt
        self.frontend_base_url = frontend_base_url
        self.from_email = from_email

    async def invite_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        role_id: UUID,
        institution_id: int | None = None,
    ) -> UserDTO:
        if await self.writer.email_exists(email):
            raise EmailAlreadyExists()

        created = await self.writer.create(
            first_name=first_name, last_name=last_name, email=email, role_id=role_id
        )

        if created.role.name == ROLE_REPRESENTATIVE:
            if institution_id is None:
                raise BadRequest(
                    "Se requiere institución educativa para el representante."
                )

            created_rep = await self.representative_writer.create(
                user_person_id=created.person_id,
                institution_id=institution_id,
            )

            if not created_rep:
                raise ConflictError(
                    message="El representante ya existe en la institución.",
                    code="REPRESENTATIVE_ALREADY_EXISTS",
                )

        token = self.jwt.encode_token(
            {
                "sub": str(created.person_id),
                "email": created.email,
                "scope": "invitation",
            },
            7200,
        )

        invite_url = f"{self.frontend_base_url}/register?token={token}"
        html_body = render_template(
            "invitation.html", {"name": first_name, "url": invite_url}
        )
        message = EmailMessage(
            subject="Invitación a registrarte en el sistema",
            body=html_body,
            from_email=self.from_email,
            to=[email],
            html=True,
        )
        self.email.send_email(message)

        created = await self.reader.get_by_id(created.person_id)
        return created
