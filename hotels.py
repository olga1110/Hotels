from fastapi import Query, Body, APIRouter
from schemas.hotel import Hotel, HotelPatch


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
]


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
def get_hotels(
        title: str | None = Query(None, description='Название отеля'),
        id: int | None = Query(None, description='Идентификатор'),
        page: int = Query(1, description='Номер страницы'),
        per_page: int = Query(5, description='Кол-во отелей на странице'),
):
    counts = get_count()
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    start = (page + counts - 2) * per_page
    return hotels_[start: start + per_page]


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
def create_hotel(
        # title: str = Body(embed=True)
        hotel_data: Hotel = Body(
            openapi_examples=
             {"1": {"summary": "Сочи", "value": {
                 "title": "Сочи у моря",
                 "name": "sochi_u_morya"
             }},
             "2": {"summary": "Дубай", "value": {
                 "title": "Дубай отель",
                 "name": "dubai_hotel"
             }}
         })
):
    global hotels
    hotels.append({'id': hotels[-1]['id']+1,
                   'title': hotel_data.title})
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