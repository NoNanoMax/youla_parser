from fastapi import APIRouter, Depends, Query
from api.deps import get_pw_res
from schemas.avto import AvtoOut
from services.avto import AvtoService
from scrapping.playwright_manager import PWResources


router = APIRouter(prefix="/avto", tags=["avto"])


@router.get("/", response_model=AvtoOut)
async def get_avto(
    url: str = Query(..., description="URL объявления"),
    res: PWResources = Depends(get_pw_res),
):
    return await AvtoService().get_by_url(res, url)
