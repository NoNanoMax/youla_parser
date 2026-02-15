
from fastapi import APIRouter
from api.v1.routers.links import router as links_router
from api.v1.routers.avto import router as avto_router


router = APIRouter()
router.include_router(links_router)
router.include_router(avto_router)