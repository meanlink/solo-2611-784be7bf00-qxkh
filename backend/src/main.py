from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.middlewares.errors import unhandled_error_handler
from src.middlewares.rate_limit import RateLimitMiddleware
from src.routes import analyses, analysis_runs, audit, auth, datasets, health, runs, workspace


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="冷链传感器相关室", lifespan=lifespan)
app.add_middleware(RateLimitMiddleware, limit=180, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(Exception, unhandled_error_handler)

for router in (health.router, auth.router, workspace.router, datasets.router,
               analyses.router, analysis_runs.router, runs.router, audit.router):
    app.include_router(router, prefix="/api")
