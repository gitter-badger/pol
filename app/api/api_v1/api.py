from fastapi import APIRouter

from app.api.api_v1.endpoints import bgm_tv

api_router = APIRouter()
api_router.include_router(bgm_tv.router, tags=['bgm.tv'])


@api_router.get('/')
def index():
    return {'detail': 'api.v1 index'}
