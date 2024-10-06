from http import HTTPStatus
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.operators import is_, is_not
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
    has_public_key: bool = None,
    in_jail: bool = None,
    sort: str = None,
) -> List[Prep]:
    """Return list of preps which is limitted to 150 records so no skip."""
    query = select(Prep)
    if penalties is not None:
        query = query.where(Prep.penalties != 0)
    if failure_count is not None:
        query = query.where(Prep.failure_count != 0)
    if not include_unregistered:
        query = query.where(Prep.grade != "0x3")
    if has_public_key is not None:
        if has_public_key:
            query = query.where(is_not(Prep.public_key, None))
        else:
            query = query.where(is_(Prep.public_key, None))

    if in_jail is not None:
        if in_jail:
            query = query.where(is_not(Prep.jail_flags, '0x0'))
        else:
            query = query.where(is_(Prep.jail_flags, '0x0'))

    if sort is not None:
        valid_sort_fields = ["name", "commission_rate", "bond_percent"]
        if sort.startswith("-"):
            sort_field = sort[1:]
            sort_order = "desc"
        else:
            sort_field = sort
            sort_order = "asc"

        if sort_field not in valid_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Invalid sort field: {sort_field}. Must "
                                        f"one of {valid_sort_fields}."
            )

        if sort_order == "desc":
            query = query.order_by(getattr(Prep, sort_field).desc())
        else:
            query = query.order_by(getattr(Prep, sort_field).asc())
    else:
        query = query.order_by(Prep.delegated.desc())

    result = await session.execute(query)
    preps = result.scalars().all()

    # Return the count in header
    response.headers["x-total-count"] = str(len(preps))

    return preps


@router.get("/governance/preps/{address}")
async def get_preps_by_address(
    address: str,
    session: AsyncSession = Depends(get_session),
) -> List[Prep]:
    """Return a single prep."""
    result = await session.execute(select(Prep).where(Prep.address == address))
    preps = result.scalars().all()

    if len(preps) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return preps
