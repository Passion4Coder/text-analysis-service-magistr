from fastapi import FastAPI
import uvicorn
from app.core.lifespan import lifespan
from app.core.config import settings

from app.analysis.router import router as analysis_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.include_router(analysis_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
