from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Bookings
from sqlalchemy import select


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    # schema = Bookings
    mapper = BookingDataMapper

    # async def check_booking_exist(self, room, date_from, date_to):
    #     query = query.filter(BookingsOrm.date_from >= date_from and BookingsOrm.date_to <= date_to)








