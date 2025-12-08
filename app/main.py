import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin.router import router as admin_router
from app.analysis.router import router as analysis_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.notes.router import router as notes_router
from app.pdf.router import router as pdf_router
from app.stats.router import router as stats_router
from app.texts.router import router as texts_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.include_router(analysis_router)
    app.include_router(texts_router)
    app.include_router(notes_router)
    app.include_router(admin_router)
    app.include_router(stats_router)
    app.include_router(pdf_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
