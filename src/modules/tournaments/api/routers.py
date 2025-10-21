from fastapi import APIRouter, Depends, status

from src.core.responses.helpers import success_response

from ..application.use_cases import AcademicYearRead
from .dependencies import provide_list_academic_years
from .schemas import AcademicYearOut

router = APIRouter()


@router.get("/academic-years")
async def get_all_academic_years(
    use_case: AcademicYearRead = Depends(provide_list_academic_years),
):
    academic_years = await use_case.retrieve_all_academic_years()
    return success_response(
        data=academic_years,
        model=AcademicYearOut,
        status_code=status.HTTP_200_OK,
    )


"""@router.get("/tournaments")
async def get_all_tournaments(
    use_case: TournamentRead = Depends(provide_list_tournaments),
):
    tournaments = await use_case.retrieve_all_tournaments()
    return success_response(
        data=tournaments,
        model=TournamentOut,
        status_code=status.HTTP_200_OK,
    )
"""
