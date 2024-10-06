from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, select

from icon_governance.db import get_session
from icon_governance.models.rewards import Reward

router = APIRouter()


@router.get("/governance/rewards/{address}")
async def get_rewards_by_address(
    response: Response,
    address: str,
    skip: int = Query(0),
    limit: int = Query(100, gt=0, lt=101),
    session: AsyncSession = Depends(get_session),
) -> List[Reward]:
    """Return list of delegations."""
    query = (
        select(Reward)
        .where(Reward.address == address)
        # .where(Reward.value != None)
        .offset(skip)
        .limit(limit)
        .order_by(Reward.timestamp.desc())
    )

    result = await session.execute(query)
    rewards = result.scalars().all()

    # Check if exists
    if len(rewards) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    query_count = select([func.count(Reward.address)]).where(Reward.address == address)
    result_count = await session.execute(query_count)
    total_count = str(result_count.scalars().all()[0])
    response.headers["x-total-count"] = total_count

    return rewards
