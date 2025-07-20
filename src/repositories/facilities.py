from datetime import date
from sqlalchemy import select, insert, delete, update

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository


from src.repositories.utils import rooms_ids_for_booking
from src.schemas.facilities import Facilities, RoomsFacilities
from src.schemas.hotel import Hotel


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities

    async def delete(self, delete_lst) -> int:
        query = select(self.model).filter(self.model.facility_id.in_(delete_lst))
        result = await self.session.execute(query)
        res = result.scalars().all()
        print(f'{res=}')
        if not res:
            return 404
        try:
            delete_stmt = delete(self.model).filter(self.model.facility_id.in_(delete_lst))
            # RoomsFacilitiesOrm.facility_id.in_(delete_lst)
            await self.session.execute(delete_stmt)
            return 200
        except:
            return 400


