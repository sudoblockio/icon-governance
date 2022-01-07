from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import select

from icon_governance.db import get_session
from icon_governance.models.proposals import Proposal

router = APIRouter()


@router.get("/governance/proposals")
async def get_proposals(
    session: AsyncSession = Depends(get_session),
) -> List[Proposal]:
    """Return list of proposals"""
    result = await session.execute(select(Proposal).order_by(Proposal.start_block_height))
    proposals = result.scalars().all()

    return proposals
