import os
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from psycopg_pool import AsyncConnectionPool

POOL: AsyncConnectionPool | None = None

async def _make_pool_with_retries(dsn: str, attempts: int = 30, delay: float = 1.0):
    last_exc = None
    for _ in range(attempts):
        try:
            pool = AsyncConnectionPool(dsn, min_size=1, max_size=5, open=False)
            await pool.open()
            return pool
        except Exception as e:
            last_exc = e
            await asyncio.sleep(delay)
    raise last_exc

@asynccontextmanager
async def lifespan(app: FastAPI):
    global POOL
    dsn = os.getenv("DATABASE_DSN")
    if not dsn:
        raise RuntimeError("DATABASE_DSN not set")
    POOL = await _make_pool_with_retries(dsn)
    try:
        yield
    finally:
        if POOL is not None:
            await POOL.close()
        await asyncio.sleep(0)

app = FastAPI(title="Analytics API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"ok": True, "msg": "Welcome"}

@app.get("/health")
async def health():
    # fast liveness (no external deps)
    return {"status": "ok"}

@app.get("/ready")
async def ready(response: Response):
    global POOL
    if POOL is None:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"ready": False, "reason": "pool-not-initialized"}
    try:
        async with POOL.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1;")
                await cur.fetchone()
        return {"ready": True}
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"ready": False, "reason": str(e)}
