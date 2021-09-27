from fastapi import APIRouter, Depends
# from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import Field, Session, SQLModel, create_engine, select

from typing import List

from icon_governance.db import get_session
from icon_governance.models.preps import Prep

router = APIRouter()


@router.get("/preps")
async def get_preps(
        session: AsyncSession = Depends(get_session)) -> List[Prep]:
    """Return list of preps"""
    result = await session.execute(select(Prep))
    preps = result.scalars().all()
    return preps
