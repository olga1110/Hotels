from datetime import date

from src.models.facilities import FacilitiesOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.facilities import Facilities
from src.schemas.hotel import Hotel


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
