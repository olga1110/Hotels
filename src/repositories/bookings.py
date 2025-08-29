from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Bookings, BookingsAdd
from sqlalchemy import select


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    # schema = Bookings
    mapper = BookingDataMapper

    # async def check_booking_exist(self, room, date_from, date_to):
    #     query = query.filter(BookingsOrm.date_from >= date_from and BookingsOrm.date_to <= date_to)

    async def add_booking(self, data: BookingsAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise Exception








