# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

from app.auth.api import routers, webhooks
from app.auth.infra.db.session import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(title="EHC Gym Auth API", lifespan=lifespan)

app.include_router(routers.router)
app.include_router(webhooks.router)
