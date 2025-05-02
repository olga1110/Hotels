from fastapi import Query, Body, APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep
from src.database import async_session_maker


from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository

from src.schemas.rooms import RoomsAdd, RoomsPatch

router = APIRouter(prefix='/hotels', tags=['Номера'])


def count(func):
    counters = {}
    def wrapper(**kwargs):
        counters[func] = counters.get(func, 0) + 1
        print(f'Функция {func.__name__} вызвана {counters[func]} раз')
        return func(counts=counters[func],  **kwargs)
    return wrapper


@count
def get_count(counts=0):
    return counts


@router.get('/{hotel_id}/rooms/',
            summary='Получение данных о номерах отеля',
            description='<h1>Получение данных о номерах по названию</h1>'
            )
async def get_rooms(
        hotel: int = Query(description='id отеля'),
        title: str | None = Query(None, description='Название номера')
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel=hotel,
            title=title
        )
      

@router.get('/{hotel_id}/rooms/{room_id}',
            summary='Получение данных о номере отеля',
            description='<h1>Получение данных о номере отеля по id</h1>')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id, id=room_id
        )


@router.delete('/{hotel_id}/rooms/{room_id}',
                summary='Удаление данных о номере отеля',
                description='<h1>Удаление данных об отеле по id</h1>'
                )
async def delete_hotels(hotel_id: int, room_id: int):
    # global hotels
    # hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    async with async_session_maker() as session:
        res = await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        if res == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в отеле {hotel_id} не найден")
        # elif res == 400:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"С id {hotel_id} найдено более 1 отеля")
        return {"status": "OK"}
    # HTTPException
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post('/{hotel_id}/rooms',
             summary='Создание номера отеля',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_room(
        # title: str = Body(embed=True)
        room_data: RoomsAdd = Body(
            openapi_examples=
             {"1": {"summary": "2-х местный", "value": {
                     "hotel_id": 20,
                     "title": "стандартный 2-х местный",
                     "description": "стандартный",
                     "price": 3000,
                     "quantity": 5
             }},
             "2": {"summary": "3-х местный", "value": {
                     "hotel_id": 23,
                     "title": "lux 3-х местный",
                     "description": "lux",
                     "price": 5000,
                     "quantity": 2
             }}
         })
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


def edit_hotel(hotel_id: int, title: str | None, name: str| None):
    global hotels
    hotel = None

    if title is None and name is None:
        return {"status": "validation error", "content": "pass at least one parameter"}
    for num, element in enumerate(hotels):
        if element['id'] == hotel_id:
            hotel = element
            num = num
            break

    if hotel is None:
        print(f'{hotels=}')
        return {"status": "OK", "content": "hotel not found"}

    if title:
        hotels[num]['title'] = title
    if name:
        hotels[num]['name'] = name
    return hotel


@router.put("/{hotel_id}/rooms/{room_id}",
            summary='Редактирование номера',
            description='<h1>Подробное описание метода</h1>'
            )
async def put_room(hotel_id: int, room_id: int, room_data: RoomsAdd):
    # return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)
    async with async_session_maker() as session:
        res = await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        if res == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в {hotel_id} не найден")
        return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary='Частичное обновление данных о номере',
            description='<h1>Подробное описание метода</h1>')
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomsPatch):
    # return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)
    async with async_session_maker() as session:
        res = await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
        if res == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Номер с id {room_id} в {hotel_id} не найден")
        return {"status": "OK"}