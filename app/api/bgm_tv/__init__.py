from fastapi import APIRouter

from . import api_v0, api_v1

router = APIRouter()
router.include_router(api_v0.router, prefix='/api.v0')
router.include_router(api_v1.router, prefix='/api.v1')
