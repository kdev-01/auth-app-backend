from typing import List

from fastapi import APIRouter, Depends, status

from src.core.responses.helpers import success_response

from ..application.use_cases import GetCities
from .dependencies import provide_list_cities
from .schemas import CityOut

router = APIRouter()

@router.get("/", response_model=List[CityOut])
async def get_all_users(
    use_case: GetCities = Depends(provide_list_cities)
):
    cities = await use_case.retrieve_all_cities()
    return success_response(
        data=cities,
        model=CityOut,
        status_code=status.HTTP_200_OK,
    )
