from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .dependencies import get_service
from .service import UserService

router = APIRouter()


@router.get("/me")
async def me(user: UserService = Depends(get_service)):
    return "Hola"
