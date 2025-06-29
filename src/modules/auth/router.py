from fastapi import APIRouter, Depends, Request, status

from src.core.responses.helpers import error_response, success_response

from .dependencies import get_service
from .schemas import UserInfo, UserLogin
from .service.auth_service import AuthService

router = APIRouter()
    
@router.post("/login", response_model=UserInfo)
async def login(
    data: UserLogin,
    service: AuthService = Depends(get_service),
):
    user, token = await service.get_user_token(data.email, data.password)
    
    response = success_response(data=user, model=UserInfo)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24,
    )
    return response

@router.get("/me/permissions", response_model=UserInfo)
async def get_user_info(
    request: Request,
    service: AuthService = Depends(get_service),
):
    try:  
        user = await service.get_user_info(request.state.user_id)
        response = success_response(data=user, model=UserInfo)
        return response
    except ValueError as e:
        return error_response(
            errors=[{"msg": str(e)}],
            message="Error al obtener información del usuario",
            status_code=status.HTTP_400_BAD_REQUEST
        )
        