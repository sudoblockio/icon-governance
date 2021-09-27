from fastapi import APIRouter
from icon_governance.api.v1.endpoints import preps

api_router = APIRouter()
api_router.include_router(preps.router)
