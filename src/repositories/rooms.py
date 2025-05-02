from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms
from sqlalchemy import select


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


