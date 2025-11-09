from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from config import settings

from analysis.router import router as analysis_router

# from database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    print("DBs ready!")
    yield
    print("DBs turn off.")


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

app.include_router(analysis_router)


@app.get("/", summary="Отримання базового шляху", tags=["Основні маршрути"])
def home():
    return {"message": "Text Analysis Service is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
