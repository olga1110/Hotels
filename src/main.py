from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.config import settings
sys.path.append(str(Path(__file__).parent.parent))


print(f'{settings.DB_NAME=}')

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_rooms)
app.include_router(router_bookings)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8920, reload=True)
