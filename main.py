from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.api import router as v1_router
from core.config import settings
from scrapping.playwright_manager import start_playwright, stop_playwright


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pw_res = await start_playwright(
        headless=settings.HEADLESS,
        max_concurrency=settings.MAX_CONCURRENCY,
    )
    yield
    await stop_playwright(app.state.pw_res)

app = FastAPI(title="Avto API", lifespan=lifespan)
app.include_router(v1_router, prefix=settings.API_PREFIX)


@app.get("/health")
def health():
    return {"status": "ok"}
