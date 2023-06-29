from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import select
from starlette.responses import Response

from icon_governance.db import get_session
from icon_governance.models.preps import Prep

router = APIRouter()


@router.get("/governance/preps")
async def get_preps(
    response: Response,
    session: AsyncSession = Depends(get_session),
    penalties: bool = None,
    failure_count: bool = None,
    include_unregistered: bool = False,
) -> List[Prep]:
    """Return list of preps which is limitted to 150 records so no skip."""
    query = select(Prep).order_by(Prep.delegated.desc())
    if penalties is not None:
        query = query.where(Prep.penalties != 0)
    if failure_count is not None:
        query = query.where(Prep.failure_count != 0)
    if not include_unregistered:
        query = query.where(Prep.grade != "0x3")
    result = await session.execute(query)
    preps = result.scalars().all()

    # Return the count in header
    response.headers["x-total-count"] = str(len(preps))

    return preps


@router.get("/governance/preps/{address}")
async def get_prep(
    address: str,
    session: AsyncSession = Depends(get_session),
) -> List[Prep]:
    """Return a single prep."""
    result = await session.execute(select(Prep).where(Prep.address == address))
    preps = result.scalars().all()

    if len(preps) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return preps
