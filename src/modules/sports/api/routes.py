from fastapi import APIRouter, Depends, status

from src.core.responses.helpers import success_response

from ..application.use_cases import SportRead
from .dependencies import provide_list_sports
from .schemas import SportOut

router = APIRouter()

@router.get("/")
async def get_all_sports(
    use_case: SportRead = Depends(provide_list_sports)
):
    sports = await use_case.retrieve_all_sports()
    return success_response(
        data=sports,
        model=SportOut,
        status_code=status.HTTP_200_OK,
    )
    