from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.database import engine

from src.schemas.hotel import Hotel, HotelPatch


router = APIRouter(prefix='/hotels', tags=['Отели'])

# hotels = [
#     {"id": 1, "title": "Sochi", "name": "sochi"},
#     {"id": 2, "title": "Дубай", "name": "dubai"},
#     {"id": 3, "title": "Мальдивы", "name": "maldivi"},
#     {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
#     {"id": 5, "title": "Москва", "name": "moscow"},
#     {"id": 6, "title": "Казань", "name": "kazan"},
#     {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
# ]


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


@router.get('',
            summary='Получение данных об отеле',
            description='<h1>Получение данных об отеле по названию</h1>'
            )
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        id: int | None = Query(None, description='Идентификатор')

):
    # counts = get_count()
    # hotels_ = []
    # for hotel in hotels:
    #     if id and hotel["id"] != id:
    #         continue
    #     if title and hotel["title"] != title:
    #         continue
    #     hotels_.append(hotel)

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        # limit = pag
        # query = (select(HotelsOrm)
        #          .filter_by(id=id, title=title)
        #          .limit(pagination.per_page)
        #          .offset(pagination.per_page*(pagination.page - 1))
        #          )
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page*(pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        print(type(hotels), hotels)
        return hotels



    # пагинация
    # start = (page + counts - 2) * per_page
    # return hotels_[start: start + per_page]
    return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]


@router.delete('/{hotel_id}',
                summary = 'Удаление данных об отеле',
                description = '<h1>Удаление данных об отеле по id</h1>'
                )
def delete_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "OK"}


@router.post('',
             summary='Создание отеля',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_hotel(
        # title: str = Body(embed=True)
        hotel_data: Hotel = Body(
            openapi_examples=
             {"1": {"summary": "Сочи", "value": {
                 "title": "Сочи у моря",
                 "location": "ул. Моря, 1"
             }},
             "2": {"summary": "Дубай", "value": {
                 "title": "Дубай отель",
                 "location": "ул. Шейха, 2"
             }}
         })
):
    # global hotels
    # hotels.append({'id': hotels[-1]['id']+1,
    #                'title': hotel_data.title})
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


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

@router.put("/{hotel_id}",
            summary='Редактирование отеля',
            description='<h1>Подробное описание метода</h1>'
            )
def put_hotel(hotel_id: int, hotel_data: Hotel):
    return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)

@router.patch("/{hotel_id}",
           summary='Частичное обновление данных об отеле',
            description='<h1>Подробное описание метода</h1>')
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)