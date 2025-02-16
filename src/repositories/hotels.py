from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset
                      ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
            # query = query.filter(HotelsOrm.location.contains(location))
            # query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title.strip()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()
