# /app/schemas/booking.py
from pydantic import BaseModel
from datetime import date
from app.models.workflow import BookingStatus

# Schema for creating a NEW booking.
# This is the "God Object" that creates the booking AND its related financials.
class BookingCreate(BaseModel):
    client_id: int
    carrier_name: str
    reference_number: str
    
    # Data for the Payable (what we owe the carrier)
    payable_amount: float
    payable_due_date: date
    
    # Data for the Invoice (what our client owes us)
    invoice_amount: float
    invoice_due_date: date

# Schema for sending a booking back to the client
class BookingPublic(BaseModel):
    id: int
    status: BookingStatus
    client_id: int
    reference_number: str
    carrier_name: str
    
    class Config:
        from_attributes = True # Updated from orm_mode in Pydantic v2
