from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (select(self.model)
                 .filter(*filter)
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        # return result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_obj_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_obj_stmt.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(add_obj_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_obj_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_obj_stmt)

    async def edit(self, data: BaseModel, exclude_unset:bool = False, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().all()
        if not res:
            return 404
        elif len(res) == 1:
            update_stmt = (update(self.model)
                           .filter_by(**filter_by)
                           .values(**data.model_dump(
                                    exclude_unset=exclude_unset))
                           )
            await self.session.execute(update_stmt)
            return 200
        else:
            return 400

    async def delete(self, **filter_by) -> int:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().all()
        print(f'{res=}')
        if not res:
            return 404
        elif len(res) == 1:
            delete_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_stmt)
            return 200
        else:
            return 400


