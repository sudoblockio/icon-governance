from fastapi import APIRouter

from icon_governance.api.v1.endpoints import (
    delegations,
    preps,
    proposals,
    rewards,
    stats,
)

api_router = APIRouter()
api_router.include_router(preps.router)
api_router.include_router(delegations.router)
api_router.include_router(proposals.router)
api_router.include_router(rewards.router)
api_router.include_router(stats.router)
