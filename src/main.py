from fastapi import FastAPI
from src.database import engine, base as Base
from src.routers import links, auth, metrics

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

metrics.add_prometheus_metrics_middleware(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(links.router)
app.include_router(metrics.router)
