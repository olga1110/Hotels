from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotel import Hotel, HotelAdd, HotelPatch


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
            summary='Получение данных об отелях',
            description='<h1>Получение данных об отеле по названию/местоположению</h1>'
            )
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Местоположение отеля'),
        date_from: date = Query(example='2024-08-01'),
        date_to: date = Query(example='2024-08-10')
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=pagination.per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to
    )

        # # limit = pag
        # # query = (select(HotelsOrm)
        # #          .filter_by(id=id, title=title)
        # #          .limit(pagination.per_page)
        # #          .offset(pagination.per_page*(pagination.page - 1))
        # #          )
        # query = select(HotelsOrm)
        # if location:
        #     query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        #     # query = query.filter(HotelsOrm.location.contains(location))
        #     # query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        # if title:
        #     # query = query.filter_by(title=title)
        #     query = query.filter(HotelsOrm.title.ilike(f'%{title.strip()}%'))
        # query = (
        #     query
        #     .limit(per_page)
        #     .offset(per_page*(pagination.page - 1))
        # )
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        # result = await session.execute(query)
        # hotels = result.scalars().all()
        # print(type(hotels), hotels)
        # return hotels

    # пагинация
    # start = (page + counts - 2) * per_page
    # return hotels_[start: start + per_page]
    return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]


@router.get('/{hotel_id}',
            summary='Получение данных об отеле',
            description='<h1>Получение данных об отеле по id</h1>')
async def get_hotel(hotel_id: int, db: DBDep,):
    # получить id, title и location
    return await db.hotels.get_one_or_none(
        id=hotel_id
    )


@router.delete('/{hotel_id}',
                summary = 'Удаление данных об отеле',
                description = '<h1>Удаление данных об отеле по id</h1>'
                )
async def delete_hotels(hotel_id: int, db: DBDep):
    # global hotels
    # hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]    
    res = await db.hotels.delete(id=hotel_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Отель с id {hotel_id} не найден")
    # elif res == 400:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"С id {hotel_id} найдено более 1 отеля")
    return {"status": "OK"}
    # HTTPException
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



@router.post('',
             summary='Создание отеля',
             description='<h1>Подробное описание метода</h1>'
             )
async def create_hotel(
        # title: str = Body(embed=True)
        db: DBDep,
        hotel_data: HotelAdd = Body(
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


def edit_hotel(hotel_id: int, title: str | None, name: str| None, db: DBDep):
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
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    # return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)    
    res = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Отель с id {hotel_id} не найден")
    # elif res == 400:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"С id {hotel_id} найдено более 1 отеля")
    return {"status": "OK"}

@router.patch("/{hotel_id}",
           summary='Частичное обновление данных об отеле',
            description='<h1>Подробное описание метода</h1>')
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    # return edit_hotel(hotel_id, hotel_data.title, hotel_data.name)    
    res = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    if res == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Отель с id {hotel_id} не найден")
    # elif res == 400:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"С id {hotel_id} найдено более 1 отеля")
    return {"status": "OK"}