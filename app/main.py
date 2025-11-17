from fastapi import FastAPI
import uvicorn
from app.core.lifespan import lifespan
from app.core.config import settings

from app.analysis.router import router as analysis_router
from app.methods.router import router as methods_router
from app.texts.router import router as texts_router
from app.notes.router import router as notes_router
from app.admin.router import router as admin_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.include_router(analysis_router)
    app.include_router(methods_router)
    app.include_router(texts_router)
    app.include_router(notes_router)
    app.include_router(admin_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
