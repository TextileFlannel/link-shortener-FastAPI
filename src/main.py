from fastapi import FastAPI
from src.database import engine, base as Base
from src.routers import links

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(links.router)