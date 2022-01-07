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


@router.get("/preps")
async def get_preps(
    session: AsyncSession = Depends(get_session),
) -> List[Prep]:
    """Return list of preps which is limitted to 150 records so no skip."""
    result = await session.execute(select(Prep).order_by(Prep.delegated.desc()))
    preps = result.scalars().all()

    return preps


@router.get("/preps/{address}")
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
