from datetime import date

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import Rooms
from sqlalchemy import select, func
from src.database import engine


def rooms_ids_for_booking(date_from: date,
                          date_to: date,
                          hotel_id: int | None = None):
    rooms_count = (select(BookingsOrm.room_id, func.count("*").label("rooms_booked")).
                   select_from(BookingsOrm).
                   filter(BookingsOrm.date_from <= date_to,
                          BookingsOrm.date_to >= date_from)
                   .group_by(BookingsOrm.room_id)
                   .cte(name="rooms_count")
                   )

    rooms_left_table = (
        select(
            RoomsOrm.id.label('room_id'),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left')

        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name='rooms_left_table')
    )

    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel))
    )

    print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={'literal_binds': True}))
    return rooms_ids_to_get


async def edit_rooms_facilities(new_facilities, room_id, db):
    facilities_lst = await db.rooms_facilities.get_filtered(room_id=room_id)
    print(f'{type(facilities_lst)=}')
    print(f'{facilities_lst=}')
    rooms_list = [i.facility_id for i in facilities_lst]
    if add_lst := list(set(new_facilities) - set(rooms_list)):
        print('создаем записи')
        rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in add_lst]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    if delete_lst := list(set(rooms_list) - set(new_facilities)):
        print('записи к удалению', delete_lst)
        # await db.rooms_facilities.delete(RoomsFacilities.facility_id.in_(delete_lst))
        await db.rooms_facilities.delete(delete_lst)






