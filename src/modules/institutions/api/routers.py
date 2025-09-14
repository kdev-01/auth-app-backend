from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from src.core.responses.helpers import success_response
from src.core.security import check_permissions

from ..application.use_cases import (
    InstitutionCreate,
    InstitutionDelete,
    InstitutionRead,
)
from .dependencies import (
    provide_delete_institution,
    provide_list_institutions,
    provider_create_institution,
)
from .schemas import InstitutionCreateInput, InstitutionOut

router = APIRouter()

@router.get("/", dependencies=[Depends(check_permissions)])
async def get_all_institutions(
    use_case: InstitutionRead = Depends(provide_list_institutions)
):
    institutions = await use_case.retrieve_all_institutions()
    return success_response(
        data=institutions,
        model=InstitutionOut,
        status_code=status.HTTP_200_OK,
    )

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_permissions)])
async def create_institution(
    data: InstitutionCreateInput,
    use_case: InstitutionCreate = Depends(provider_create_institution)
):
    institution = await use_case.create_institution(
        name=data.name,
        city_id=data.city_id
    )
    
    return success_response(
        data=institution,
        model=InstitutionOut,
        status_code=status.HTTP_201_CREATED,
        message="¡La institución educativa fue registrada con éxito!"
    )
    
@router.delete("/{institution_id}/affiliation", dependencies=[Depends(check_permissions)])
async def delete_institution(
    institution_id: int,
    use_case: InstitutionDelete = Depends(provide_delete_institution),
):
    await use_case.delete(
        target_id=institution_id,
    )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
