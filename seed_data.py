"""
Seed script to populate the database with dummy data.
Run this with: python seed_data.py
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session, engine, Base
from app.models.organization import Organization, User
from app.models.client import Client
from app.models.workflow import Booking, BookingStatus
from app.models.finance import Payable, Invoice, FinancingRequest, PaymentStatus, FinancingStatus


async def seed_database():
    """Seed the database with dummy data."""
    
    async with async_session() as session:
        # Create Organizations
        org1 = Organization(name="Global Freight Solutions")
        org2 = Organization(name="Pacific Logistics Co")
        session.add_all([org1, org2])
        await session.flush()
        
        print(f"Created organizations: {org1.name}, {org2.name}")
        
        # Create Users
        user1 = User(
            email="john@globalfreight.com",
            hashed_password="hashed_password_123",
            organization_id=org1.id
        )
        user2 = User(
            email="sarah@globalfreight.com",
            hashed_password="hashed_password_456",
            organization_id=org1.id
        )
        user3 = User(
            email="mike@pacificlogistics.com",
            hashed_password="hashed_password_789",
            organization_id=org2.id
        )
        session.add_all([user1, user2, user3])
        await session.flush()
        
        print(f"Created {3} users")
        
        # Create Clients for Org 1
        client1 = Client(
            name="Acme Manufacturing",
            organization_id=org1.id
        )
        client2 = Client(
            name="TechStart Industries",
            organization_id=org1.id
        )
        client3 = Client(
            name="GreenEnergy Corp",
            organization_id=org1.id
        )
        
        # Create Clients for Org 2
        client4 = Client(
            name="AutoParts Inc",
            organization_id=org2.id
        )
        session.add_all([client1, client2, client3, client4])
        await session.flush()
        
        print(f"Created {4} clients")
        
        # Create Bookings with Payables and Invoices for Org 1
        bookings_data = [
            {
                "client": client1,
                "carrier": "Maersk",
                "ref": "BOOK-2025-001",
                "status": BookingStatus.CONFIRMED,
                "payable_amount": 15000.00,
                "invoice_amount": 16500.00,
                "days_offset": -10
            },
            {
                "client": client1,
                "carrier": "CMA CGM",
                "ref": "BOOK-2025-002",
                "status": BookingStatus.COMPLETED,
                "payable_amount": 22000.00,
                "invoice_amount": 24200.00,
                "days_offset": -5
            },
            {
                "client": client2,
                "carrier": "MSC",
                "ref": "BOOK-2025-003",
                "status": BookingStatus.PENDING,
                "payable_amount": 8500.00,
                "invoice_amount": 9350.00,
                "days_offset": 5
            },
            {
                "client": client3,
                "carrier": "Hapag-Lloyd",
                "ref": "BOOK-2025-004",
                "status": BookingStatus.CONFIRMED,
                "payable_amount": 31000.00,
                "invoice_amount": 34100.00,
                "days_offset": 10
            },
            {
                "client": client2,
                "carrier": "ONE",
                "ref": "BOOK-2025-005",
                "status": BookingStatus.PENDING,
                "payable_amount": 12500.00,
                "invoice_amount": 13750.00,
                "days_offset": 15
            },
        ]
        
        bookings = []
        payables = []
        for data in bookings_data:
            booking = Booking(
                client_id=data["client"].id,
                carrier_name=data["carrier"],
                reference_number=data["ref"],
                status=data["status"],
                organization_id=org1.id
            )
            session.add(booking)
            await session.flush()
            
            # Create Payable
            payable_due = datetime.now() + timedelta(days=data["days_offset"])
            payable = Payable(
                booking_id=booking.id,
                amount=data["payable_amount"],
                due_date=payable_due,
                payee_name=data["carrier"],
                status=PaymentStatus.PENDING
            )
            session.add(payable)
            await session.flush()
            payables.append(payable)
            
            # Create Invoice
            invoice_due = datetime.now() + timedelta(days=data["days_offset"] + 15)
            invoice = Invoice(
                booking_id=booking.id,
                client_id=data["client"].id,
                amount=data["invoice_amount"],
                due_date=invoice_due,
                status=PaymentStatus.PENDING
            )
            session.add(invoice)
            
            bookings.append(booking)
        
        await session.flush()
        print(f"Created {len(bookings)} bookings with payables and invoices")
        
        # Create some Financing Requests for the first 3 bookings
        financing_data = [
            {
                "booking_index": 0,
                "status": FinancingStatus.FUNDED,
                "requested_days_ago": 12,
                "approved_days_ago": 11,
                "funded_days_ago": 10
            },
            {
                "booking_index": 1,
                "status": FinancingStatus.APPROVED,
                "requested_days_ago": 6,
                "approved_days_ago": 5,
                "funded_days_ago": None
            },
            {
                "booking_index": 3,
                "status": FinancingStatus.PENDING,
                "requested_days_ago": 2,
                "approved_days_ago": None,
                "funded_days_ago": None
            },
        ]
        
        for fin_data in financing_data:
            booking = bookings[fin_data["booking_index"]]
            payable = payables[fin_data["booking_index"]]
            
            # Find payable amount from our data
            payable_amount = bookings_data[fin_data["booking_index"]]["payable_amount"]
            invoice_amount = bookings_data[fin_data["booking_index"]]["invoice_amount"]
            
            fee_amount = payable_amount * 0.025  # 2.5% fee
            
            financing = FinancingRequest(
                payable_id=payable.id,
                amount_requested=payable_amount,
                fee_percentage=2.5,
                fee_amount=fee_amount,
                total_repayment=invoice_amount,
                status=fin_data["status"],
                requested_at=datetime.now() - timedelta(days=fin_data["requested_days_ago"]),
                approved_at=datetime.now() - timedelta(days=fin_data["approved_days_ago"]) if fin_data["approved_days_ago"] else None,
                funded_at=datetime.now() - timedelta(days=fin_data["funded_days_ago"]) if fin_data["funded_days_ago"] else None
            )
            session.add(financing)
        
        await session.flush()
        print(f"Created {len(financing_data)} financing requests")
        
        # Create one booking for Org 2
        booking_org2 = Booking(
            client_id=client4.id,
            carrier_name="COSCO",
            reference_number="BOOK-2025-PAC-001",
            status=BookingStatus.CONFIRMED,
            organization_id=org2.id
        )
        session.add(booking_org2)
        await session.flush()
        
        payable_org2 = Payable(
            booking_id=booking_org2.id,
            amount=18000.00,
            due_date=datetime.now() + timedelta(days=20),
            payee_name="COSCO",
            status=PaymentStatus.PENDING
        )
        session.add(payable_org2)
        
        invoice_org2 = Invoice(
            booking_id=booking_org2.id,
            client_id=client4.id,
            amount=19800.00,
            due_date=datetime.now() + timedelta(days=35),
            status=PaymentStatus.PENDING
        )
        session.add(invoice_org2)
        
        print(f"Created 1 booking for organization 2")
        
        # Commit all changes
        await session.commit()
        print("\nDatabase seeding completed successfully!")
        print("\nSummary:")
        print(f"  - 2 Organizations")
        print(f"  - 3 Users")
        print(f"  - 4 Clients")
        print(f"  - 6 Bookings")
        print(f"  - 6 Payables")
        print(f"  - 6 Invoices")
        print(f"  - 3 Financing Requests")


async def main():
    print("Starting database seeding...\n")
    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
