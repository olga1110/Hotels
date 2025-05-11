from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, description='Номер страницы', ge=1)]
    per_page: Annotated[int, Query(5, description='Кол-во отелей на странице', ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthServices().decode_token(token)
    return data['user_id']

UserIdDep = Annotated[id, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]

