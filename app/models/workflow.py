# /app/models/workflow.py
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class BookingStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"

class Booking(Base):
    """
    The core "Shipment" or "Job".
    Tied to an Organization and one of their Clients.
    """
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="bookings")
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client")
    
    reference_number = Column(String, unique=True, index=True)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    carrier_name = Column(String)

    # Financial objects linked to this one booking
    payable = relationship("Payable", back_populates="booking", uselist=False)
    invoice = relationship("Invoice", back_populates="booking", uselist=False)
