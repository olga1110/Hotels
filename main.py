from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get('/hotels')
def get_hotels(
        title: str | None = Query(None, description='Название отеля'),
        id: int | None = Query(None, description='Идентификатор')
):
    return [hotel for hotel in hotels if hotel['title'] == title]


@app.delete('/hotels/{hotel_id}')
def delete_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "OK"}


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({'id': hotels[-1]['id']+1,
                   'title': title})
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
        hotels[num]['name']  = name
    return hotel

@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    return edit_hotel(hotel_id, title, name)

@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, title: str | None = Body(None), name: str| None= Body(None)):
    return edit_hotel(hotel_id, title, name)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
