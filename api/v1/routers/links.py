from fastapi import APIRouter, Depends
from api.deps import get_pw_res
from schemas.link import LinkOut
from services.links import LinksService
from scrapping.playwright_manager import PWResources


router = APIRouter(prefix="/links", tags=["links"])


@router.get("/", response_model=list[LinkOut])
async def list_links(
    query: str | None = None,
    res: PWResources = Depends(get_pw_res),
):
    return await LinksService().list_links(res, query=query)
