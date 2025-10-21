from fastapi import APIRouter, Depends, Request, status

from src.core.responses.helpers import success_response
from src.core.security.permissions import check_permissions

from ..application.use_cases import AuthenticateUser, GetUserSession, RoleRead
from .dependencies import (
    provider_authenticate_user,
    provider_list_roles,
    provider_user_session,
)
from .schemas import RoleOut, UserLoginInput, UserOut

router = APIRouter()


@router.get("/logout")
def logout():
    response = success_response(message="Sesión cerrada correctamente.")
    response.delete_cookie(key="access_token")
    return response


@router.get("/me/session")
async def get_permissions(
    request: Request,
    use_case: GetUserSession = Depends(provider_user_session),
):
    session = await use_case.get_session(request.state.user_id)
    return success_response(
        data=session,
        model=UserOut,
        status_code=status.HTTP_200_OK,
    )


@router.get("/roles", dependencies=[Depends(check_permissions)])
async def get_all_roles(use_case: RoleRead = Depends(provider_list_roles)):
    roles = await use_case.retrieve_all_roles()
    return success_response(
        data=roles,
        model=RoleOut,
        status_code=status.HTTP_200_OK,
    )


@router.post("/login")
async def login(
    data: UserLoginInput,
    use_case: AuthenticateUser = Depends(provider_authenticate_user),
):
    user, token = await use_case.login(data.email, data.password)

    response = success_response(
        data=user,
        model=UserOut,
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24,
    )
    return response
