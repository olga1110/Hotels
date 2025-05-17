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
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingsAdd(price=room_price, user_id=user_id, **booking_data.model_dump(exclude_unset=True))
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get('',
            summary='Получение данных о всех бронированиях'
            )
async def get_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.get('/me',
            summary='Получение данных о бронированиях пользователя'
            )
async def get_bookings(db: DBDep, ):
    return await db.bookings.get_all()