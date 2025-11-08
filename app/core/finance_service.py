# /app/core/finance_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.finance import Payable, FinancingRequest, FinancingStatus
from app.models.workflow import Booking
from app.models.organization import Organization
import datetime

class FinanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_payable(self, payable_id: int, org: Organization) -> Payable | None:
        """
        Get a single payable, ensuring it belongs to the org.
        """
        result = await self.db.execute(
            select(Payable)
            .join(Payable.booking) # Join to check organization_id
            .where(
                Payable.id == payable_id,
                Booking.organization_id == org.id
            )
        )
        return result.scalars().first()

    async def request_financing(self, payable: Payable) -> FinancingRequest:
        """
        Core business logic: Create a new FinancingRequest for a Payable.
        """
        # 1. TODO: Check for existing requests
        # 2. TODO: Run basic underwriting rules (e.g., is amount > $1M?)

        # Calculate fees (example: 2.5% fee)
        fee_amount = payable.amount * 0.025
        
        # We collect the full invoice amount from the client
        # We need to find the invoice associated with this payable's booking
        # For simplicity, we'll assume invoice amount = payable + profit (hardcoded)
        # In a real app, we'd fetch the linked Invoice.amount
        total_repayment = payable.amount * 1.05 # Placeholder

        new_request = FinancingRequest(
            payable_id=payable.id,
            amount_requested=payable.amount,
            fee_percentage=2.5,
            fee_amount=fee_amount,
            total_repayment=total_repayment,
            status=FinancingStatus.PENDING,
            requested_at=datetime.datetime.utcnow()
        )
        
        self.db.add(new_request)
        await self.db.commit()
        await self.db.refresh(new_request)
        return new_request
