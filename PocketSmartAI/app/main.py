from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, settings
from app.db import init_db
from app.routes import (
    auth,
    pages,
    planners,
    session,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_origin,
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR
            / "app"
            / "static"
        )
    ),
    name="static",
)


app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(session.router)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": settings.app_name,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "model": settings.gemini_model,
    }


@app.get("/startup")
def startup_status():

    return health()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )