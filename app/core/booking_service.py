# /app/core/booking_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.workflow import Booking
from app.models.finance import Payable, Invoice
from app.models.organization import Organization
from app.schemas.booking import BookingCreate

class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(
        self, booking_data: BookingCreate, org: Organization
    ) -> Booking:
        """
        Core business logic: Create a Booking, its associated
        Payable, and its associated Invoice in a single transaction.
        """
        # Create the main booking object
        new_booking = Booking(
            client_id=booking_data.client_id,
            carrier_name=booking_data.carrier_name,
            reference_number=booking_data.reference_number,
            organization_id=org.id,
            status="PENDING"
        )
        self.db.add(new_booking)
        await self.db.flush() # Flush to get the new_booking.id

        # Create the Payable (bill from carrier)
        new_payable = Payable(
            booking_id=new_booking.id,
            amount=booking_data.payable_amount,
            due_date=booking_data.payable_due_date,
            payee_name=booking_data.carrier_name,
            status="PENDING"
        )
        
        # Create the Invoice (bill to our client)
        new_invoice = Invoice(
            booking_id=new_booking.id,
            client_id=booking_data.client_id,
            amount=booking_data.invoice_amount,
            due_date=booking_data.invoice_due_date,
            status="PENDING"
        )
        
        self.db.add_all([new_payable, new_invoice])
        await self.db.commit()
        await self.db.refresh(new_booking)
        return new_booking

    async def get_bookings(self, org: Organization) -> list[Booking]:
        """
        Get all bookings for a given organization.
        """
        result = await self.db.execute(
            select(Booking).where(Booking.organization_id == org.id)
        )
        return result.scalars().all()
