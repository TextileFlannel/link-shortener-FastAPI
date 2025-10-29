from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from src import models, schemas
import string
import random

def gen_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def create_link(db: AsyncSession, link: schemas.LinkRequest) -> models.Link:
    short_code = gen_short_code()

    existing_link = await get_link_by_short_code(db, short_code)
    while existing_link:
        short_code = gen_short_code()
        existing_link = await get_link_by_short_code(db, short_code)

    db_link = models.Link(
        original_url=link.original_url,
        short_code=short_code
    )

    db.add(db_link)
    await db.commit()
    await db.refresh(db_link)
    return db_link

async def get_link_by_short_code(db: AsyncSession, short_code: str) -> models.Link:
    result = await db.execute(
        select(models.Link).where(models.Link.short_code == short_code)
    )
    return result.scalar_one_or_none()

async def get_link_by_id(db: AsyncSession, link_id: int) -> models.Link:
    result = await db.execute(
        select(models.Link).where(models.Link.id == link_id)
    )
    return result.scalar_one_or_none()

async def increment_click_count(db: AsyncSession, link_id: int):
    link = await get_link_by_id(db, link_id)
    if link:
        link.click_count += 1
        await db.commit()

async def create_click(db: AsyncSession, click: schemas.ClickRequest, link_id: int) -> models.Click:
    db_click = models.Click(
        link_id=link_id,
        ip_address=click.ip_address,
        user_agent=click.user_agent
    )
    db.add(db_click)
    await db.commit()
    await db.refresh(db_click)
    return db_click

async def get_all_links(db: AsyncSession):
    result = await db.execute(
        select(models.Link)
    )
    return result.scalars().all()

async def delete_link_by_short_code(db: AsyncSession, short_code: str) -> bool:
    link = await get_link_by_short_code(db, short_code)
    if not link:
        return False

    await db.execute(
        delete(models.Click).where(models.Click.link_id == link.id)
    )

    result = await db.execute(
        delete(models.Link).where(models.Link.id == link.id)
    )

    await db.commit()
    return result.rowcount > 0