import pytest
import json
import os
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool

from src.main import app
from src.models import *
from src.schemas.hotel import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager


# @pytest.fixture(scope="session", autouse=True)
# # async def async_main():
#     print("Я ФИКСТУРА")
#     # проверка перед изменениями в БД
#     assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_add_data():
    with open(os.path.join('tests', 'mock_hotels.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(os.path.join('tests', 'mock_rooms.json'), 'r', encoding='utf-8') as f:
        rooms_data = json.load(f)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel in data:
            hotel_data = HotelAdd(title=hotel['title'], location=hotel['location'])
            new_hotel_data = await db.hotels.add(hotel_data)
            print(f"{new_hotel_data=}")
            await db.commit()
        for room in rooms_data:
            #         "hotel_id": 1,
            #         "title": "Улучшенный с террасой и видом на озеро",
            #         "description": "Невероятный красоты номер.",
            #         "price": 24500,
            #         "quantity": 5
            room_data = RoomsAdd(hotel_id=room['hotel_id'], title=room['title'], description=room['description'],
                                 price=room['price'], quantity=room['quantity'])

            new_room_data = await db.rooms.add(room_data)
            print(f"{new_room_data=}")
            await db.commit()





@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )