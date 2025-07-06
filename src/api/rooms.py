from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException, status

from src.api.dependencies import DBDep
from src.database import async_session_maker



from src.repositories.rooms import RoomsRepository

from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, RoomsPatchRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


# @router.get('/{hotel_id}/rooms/',
#             summary='Получение данных о номерах отеля',
#             description='<h1>Получение данных о номерах по названию</h1>'
#             )
# async def get_rooms(
#         db: DBDep,
#         hotel: int = Query(description='id отеля'),
#         title: str | None = Query(None, description='Название номера')
#
# ):
#     return await db.rooms.get_all(
#         hotel=hotel,
#         title=title
#     )


@router.get('/{hotel_id}/rooms/',
            summary='Получение данных о номерах отеля',
            description='<h1>Получение данных о номерах по названию</h1>'
            )
async def get_rooms(
        db: DBDep,
        hotel: int = Query(description='id отеля'),
        # title: str | None = Query(None, description='Название номера'),
        date_from: date = Query(example='2024-08-01'),
        date_to: date = Query(example='2024-08-10')
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel, date_from=date_from, date_to=date_to
    )
      

@router.get('/{hotel_id}/rooms/{room_id}',
            summary='Получение данных о номере отеля',
            description='<h1>Получение данных о номере отеля по id</h1>')
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(
        hotel_id=hotel_id, id=room_id
    )


@router.delete('/{hotel_id}/rooms/{room_id}',
                summary='Удаление данных о номере отеля',
                description='<h1>Удаление данных об отеле по id</h1>'
                )
async def delete_hotels(hotel_id: int, room_id: int, db: DBDep):
    res = await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в отеле {hotel_id} не найден")
    # elif res == 400:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"С id {hotel_id} найдено более 1 отеля")
    return {"status": "OK"}


@router.post('/{hotel_id}/rooms',
             summary='Создание номера отеля',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_room(hotel_id: int, db: DBDep,
        room_data: RoomsAddRequest = Body(
            openapi_examples=
             {"1": {"summary": "2-х местный", "value": {
                     "title": "стандартный 2-х местный",
                     "description": "стандартный",
                     "price": 3000,
                     "quantity": 5
             }},
             "2": {"summary": "3-х местный", "value": {
                     "title": "lux 3-х местный",
                     "description": "lux",
                     "price": 5000,
                     "quantity": 2
             }}
         })
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary='Редактирование номера',
            description='<h1>Подробное описание метода</h1>'
            )
async def put_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest, db: DBDep):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    res = await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в {hotel_id} не найден")
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary='Частичное обновление данных о номере',
            description='<h1>Подробное описание метода</h1>')
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomsPatchRequest, db: DBDep):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    res = await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в {hotel_id} не найден")
    return {"status": "OK"}