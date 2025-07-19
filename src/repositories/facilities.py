from datetime import date

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
