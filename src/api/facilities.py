from fastapi import Query, Body, APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep, DBDep, UserIdDep
from src.schemas.facilities import FacilitiesAdd

from datetime import date

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('',
            summary='Получение списка удобств'
            )
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('',
             summary='Добавление удобства',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_facility(db: DBDep,
        facility_data: FacilitiesAdd = Body(
            openapi_examples=
             {"1": {"summary": "удобство", "value": {
                     "title": "туалет"
             }}
         })
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
