from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, select

from icon_governance.db import get_session
from icon_governance.models.apy_time import ApyTime
from icon_governance.models.commission_time import CommissionTime
from icon_governance.models.stats import Stats

router = APIRouter()


@router.get("/governance/stats/apy/time")
async def get_apy_over_time(
    response: Response,
    start_timestamp: int = None,
    end_timestamp: int = None,
    skip: int = Query(0),
    limit: int = Query(100, gt=0, lt=101),
    session: AsyncSession = Depends(get_session),
) -> List[ApyTime]:
    """
    Return a time series of APY over time along with other governance stats like total
     delegation / stake and the governance variables needed derive APY.
    """
    query = select(ApyTime).offset(skip).limit(limit).order_by(ApyTime.timestamp.desc())

    if start_timestamp is not None:
        query = query.where(ApyTime.timestamp >= start_timestamp)
    if end_timestamp is not None:
        query = query.where(ApyTime.timestamp <= end_timestamp)

    result = await session.execute(query)
    apy_time_series = result.scalars().all()

    # Check if exists
    if len(apy_time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    total_count = str(len(apy_time_series))
    response.headers["x-total-count"] = total_count

    return apy_time_series


@router.get("/governance/stats/commission/time")
async def get_commission_over_time(
    response: Response,
    start_timestamp: int = None,
    end_timestamp: int = None,
    skip: int = Query(0),
    limit: int = Query(1000, gt=0, lt=1001),
    session: AsyncSession = Depends(get_session),
) -> List[CommissionTime]:
    """Return a time series of commission statistics over time."""
    query = select(CommissionTime).offset(skip).limit(limit).order_by(
        CommissionTime.timestamp.desc()
    )

    if start_timestamp is not None:
        query = query.where(ApyTime.timestamp >= start_timestamp)
    if end_timestamp is not None:
        query = query.where(ApyTime.timestamp <= end_timestamp)

    result = await session.execute(query)
    commission_time_series = result.scalars().all()

    # Check if exists
    if len(commission_time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    total_count = str(len(commission_time_series))
    response.headers["x-total-count"] = total_count

    return commission_time_series


@router.get("/governance/stats")
async def get_governance_stats(
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> List[Stats]:
    """Get stats - single entry json."""
    query = select(Stats).limit(1).order_by(Stats.timestamp.desc())

    result = await session.execute(query)
    stats = result.scalars().first()

    return stats
