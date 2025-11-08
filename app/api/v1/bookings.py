# /app/api/v1/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.organization import Organization
from app.core.auth_service import get_current_organization
from app.schemas.booking import BookingCreate, BookingPublic
from app.core.booking_service import BookingService

router = APIRouter()

# Dependency to get the service
def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(db)

@router.post("/", response_model=BookingPublic)
async def create_booking(
    booking_in: BookingCreate,
    organization_id: int = Depends(get_current_organization),
    service: BookingService = Depends(get_booking_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new Booking, its Payable, and its Invoice.
    """
    # Get the organization object
    result = await db.execute(
        select(Organization).where(Organization.id == organization_id)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # TODO: Validate that booking_in.client_id belongs to this org
    
    booking = await service.create_booking(booking_data=booking_in, org=org)
    return booking

@router.get("/", response_model=List[BookingPublic])
async def list_bookings(
    organization_id: int = Depends(get_current_organization),
    service: BookingService = Depends(get_booking_service),
    db: AsyncSession = Depends(get_db)
):
    """
    List all bookings for the user's organization.
    """
    # Get the organization object
    result = await db.execute(
        select(Organization).where(Organization.id == organization_id)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    bookings = await service.get_bookings(org=org)
    return bookings
