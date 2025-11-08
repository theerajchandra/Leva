"""
Add demo bookings for the demo@leva.com user (organization_id=6)
"""
import asyncio
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
# Import organization first to resolve relationships
from app.models.organization import Organization, User
from app.models.client import Client
from app.models.workflow import Booking, BookingStatus
from app.models.finance import Payable, Invoice, PaymentStatus


async def add_demo_data():
    async with async_session() as session:
        # Create demo client
        client = Client(
            name="ABC Manufacturing",
            organization_id=6
        )
        session.add(client)
        await session.flush()
        print(f"✓ Created client: {client.name}")
        
        # Create 3 demo bookings
        bookings_data = [
            {
                "carrier": "Maersk Line",
                "ref": "BK-2024-001",
                "status": BookingStatus.CONFIRMED,
                "payable": 5000.00,
                "invoice": 6500.00
            },
            {
                "carrier": "MSC Shipping",
                "ref": "BK-2024-002",
                "status": BookingStatus.PENDING,
                "payable": 8000.00,
                "invoice": 10500.00
            },
            {
                "carrier": "CMA CGM",
                "ref": "BK-2024-003",
                "status": BookingStatus.COMPLETED,
                "payable": 3500.00,
                "invoice": 4500.00
            }
        ]
        
        for idx, data in enumerate(bookings_data):
            booking = Booking(
                client_id=client.id,
                carrier_name=data["carrier"],
                reference_number=data["ref"],
                status=data["status"],
                organization_id=6
            )
            session.add(booking)
            await session.flush()
            
            # Create payable
            payable = Payable(
                booking_id=booking.id,
                amount=data["payable"],
                due_date=date.today() + timedelta(days=30),
                status=PaymentStatus.PENDING
            )
            session.add(payable)
            
            # Create invoice
            invoice = Invoice(
                booking_id=booking.id,
                client_id=client.id,
                amount=data["invoice"],
                due_date=date.today() + timedelta(days=60),
                status=PaymentStatus.PENDING
            )
            session.add(invoice)
            
            print(f"✓ Created booking: {data['ref']} - {data['carrier']}")
        
        await session.commit()
        print("\n✓ Demo data added successfully!")
        print("Login with: demo@leva.com / demo123")


if __name__ == "__main__":
    asyncio.run(add_demo_data())
