# /app/api/v1/finance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.organization import Organization
from app.core.auth_service import get_current_organization
from app.schemas.finance import FinancingRequestPublic
from app.core.finance_service import FinanceService

router = APIRouter()

# Dependency to get the service
def get_finance_service(db: AsyncSession = Depends(get_db)) -> FinanceService:
    return FinanceService(db)

@router.post(
    "/payables/{payable_id}/request_financing", 
    response_model=FinancingRequestPublic
)
async def request_financing(
    payable_id: int,
    organization_id: int = Depends(get_current_organization),
    service: FinanceService = Depends(get_finance_service),
    db: AsyncSession = Depends(get_db)
):
    """
    This is the "FINANCE THIS" button.
    Creates a new FinancingRequest for a specific Payable.
    """
    # Get the organization object
    result = await db.execute(
        select(Organization).where(Organization.id == organization_id)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # 1. Get the payable and ensure it belongs to this org
    payable = await service.get_payable(payable_id=payable_id, org=org)
    if not payable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Payable not found"
        )
    
    # 2. Call the service logic to create the request
    # TODO: Add check to prevent duplicate requests
    
    financing_request = await service.request_financing(payable=payable)
    return financing_request
