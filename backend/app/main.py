from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.agents import router as agents_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.runs import router as runs_router
from app.api.v1.stream import router as stream_router
from app.api.dependencies import startup_registry
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Executor with File Data",
        description="Upload a file, paste a curl command — we call your API for every record automatically.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(agents_router, prefix="/api/v1")
    app.include_router(tasks_router, prefix="/api/v1")
    app.include_router(runs_router, prefix="/api/v1")
    app.include_router(stream_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup():
        startup_registry()

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
