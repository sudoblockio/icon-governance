from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, select

from icon_governance.db import get_session
from icon_governance.models.delegations import Delegation

router = APIRouter()


@router.get("/governance/delegations/{address}")
async def get_delegations(
    response: Response,
    address: str,
    skip: int = Query(0),
    limit: int = Query(100, gt=0, lt=101),
    session: AsyncSession = Depends(get_session),
) -> List[Delegation]:
    """Return list of delegations."""
    query = (
        select(Delegation)
        .where(Delegation.address == address)
        .offset(skip)
        .limit(limit)
        .order_by(Delegation.value)
    )

    result = await session.execute(query)
    delegations = result.scalars().all()

    # Check if exists
    if len(delegations) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    query_count = select([func.count(Delegation.address)]).where(Delegation.address == address)
    result_count = await session.execute(query_count)
    total_count = str(result_count.scalars().all()[0])
    response.headers["x-total-count"] = total_count

    return delegations


@router.get("/governance/votes/{address}")
async def get_delegations(
    address: str,
    response: Response,
    skip: int = Query(0),
    limit: int = Query(100, gt=0, lt=101),
    session: AsyncSession = Depends(get_session),
) -> List[Delegation]:
    """Return list of votes."""
    query = (
        select(Delegation)
        .where(Delegation.prep_address == address)
        .offset(skip)
        .limit(limit)
        .order_by(Delegation.value)
    )

    result = await session.execute(query)
    delegations = result.scalars().all()

    # Check if exists
    if len(delegations) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    query_count = select([func.count(Delegation.address)])
    result_count = await session.execute(query_count)
    total_count = str(result_count.scalars().all()[0])
    response.headers["x-total-count"] = total_count

    return delegations
