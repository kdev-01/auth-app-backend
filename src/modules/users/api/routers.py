from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import Response

from src.core.responses.helpers import success_response
from src.core.security import check_permissions

from ..application.use_cases import InviteUser, UserDelete, UserRead
from .dependencies import provide_delete_user, provide_invite_user, provide_list_users
from .schemas import UserInvite, UserOut

router = APIRouter()


@router.get("/", dependencies=[Depends(check_permissions)])
async def get_all_users(
    request: Request, use_case: UserRead = Depends(provide_list_users)
):
    users = await use_case.retrieve_all_users(exclude_user_id=request.state.user_id)

    return success_response(
        data=users,
        model=UserOut,
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/invitation",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_permissions)],
)
async def invite_user(
    data: UserInvite,
    use_case: InviteUser = Depends(provide_invite_user),
):
    user = await use_case.invite_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        role_id=data.role_id,
        institution_id=data.institution_id,
    )

    return success_response(
        data=user,
        model=UserOut,
        status_code=status.HTTP_201_CREATED,
        message="¡La invitación fue enviada con éxito!",
    )


@router.delete("/{person_id}", dependencies=[Depends(check_permissions)])
async def delete_user(
    person_id: UUID,
    request: Request,
    use_case: UserDelete = Depends(provide_delete_user),
):
    await use_case.delete(
        target_id=person_id,
        requester_id=request.state.user_id,
        requester_role=request.state.role,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
