from fastapi import Query, Body, APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep, DBDep, UserIdDep
from src.schemas.bookings import Bookings, BookingsAdd, BookingsAddRequest

from datetime import date

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('',
             summary='Создание бронирования',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingsAddRequest = Body(
            openapi_examples=
             {"1": {"summary": "Бронь1", "value": {
                 "room_id": 1,
                 "date_from": date(2025, 5, 15),
                 "date_to": date(2025, 5, 25)
             }},
             "2": {"summary": "Бронь2", "value": {
                 "room_id": 3,
                 "date_from": date(2025, 6, 15),
                 "date_to": date(2025, 6, 16)
             }}
         })
):
    await db.bookings.get_price()
    _booking_data = BookingsAdd(price=db.bookings.model.total_cost, user_id=user_id, **booking_data.model_dump(exclude_unset=True))
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}