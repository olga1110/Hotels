from datetime import date

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Rooms
from sqlalchemy import select, func
from src.database import engine


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all(self,
                      hotel,
                      title
                      ) -> list[Rooms]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel)
        if title:
            query = query.filter(RoomsOrm.title.ilike(f'%{title.strip()}%'))
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        # return result.scalars().all()
        return [Rooms.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_from: date,
                                   date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id, date_from, date_to)
        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={'literal_binds': True}))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))