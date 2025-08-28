from datetime import date

from src.schemas.bookings import BookingsAdd
from src.schemas.facilities import FacilitiesAdd


async def test_facilities_crud(db):
    facility_data = FacilitiesAdd(title='Кондей')
    new_facility = await db.facilities.add(facility_data)

    # получить эту удобство и убедиться что оно есть
    facility = await db.facilities.get_one_or_none(id=new_facility.id)
    print(f'{facility=}')
    print(f'{new_facility.id=}')
    assert facility
    assert facility.id == new_facility.id

    #
    # # обновить бронь
    # updated_date = date(year=2024, month=8, day=25)
    # update_booking_data = BookingsAdd(
    #     user_id=user_id,
    #     room_id=room_id,
    #     date_from=date(year=2024, month=8, day=10),
    #     date_to=updated_date,
    #     price=100,
    # )
    # update_facilities_data = FacilitiesAdd(title='Кондиционер')
    # await db.bookings.edit(update_booking_data, id=new_booking.id)
    # updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    # assert updated_booking
    # assert updated_booking.id == new_booking.id
    # assert updated_booking.date_to == updated_date
    #
    # # удалить бронь
    # await db.bookings.delete(id=new_booking.id)
    # booking = await db.bookings.get_one_or_none(id=new_booking.id)
    # assert not booking