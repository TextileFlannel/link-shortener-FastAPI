from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud, schemas, models
from src.database import get_db
from src.schemas import AllLinksResponse
from src.auth import get_current_user

router = APIRouter()

@router.post('/shorten', response_model=schemas.LinkResponse)
async def create_short_url(
        link: schemas.LinkRequest,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.create_link(db, link, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/go/{short_code}')
async def redirect_to_original(
        request: Request,
        short_code: str,
        db: AsyncSession = Depends(get_db)
):
    link = await crud.get_link_by_short_code(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail='not found')

    await crud.increment_click_count(db, link.id)

    click_data = schemas.ClickRequest(
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    await crud.create_click(db, click_data, link.id)

    return RedirectResponse(link.original_url)

@router.get('/link/{short_code}/info', response_model=schemas.LinkResponse)
async def get_link_info(
        short_code: str,
        db: AsyncSession = Depends(get_db)
):
    link = await crud.get_link_by_short_code(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail='not found')
    return link

@router.delete('/link/{short_code}')
async def delete_link(
        short_code: str,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_link_by_short_code(db, short_code, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail='not found or not authorized')

    return {'message': 'link is delete'}

@router.get('/links', response_model=AllLinksResponse)
async def get_all_links(db: AsyncSession = Depends(get_db)):
    links = await crud.get_all_links(db)
    return {"links": links}