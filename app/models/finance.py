# /app/models/finance.py
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FINANCED = "FINANCED"
    OVERDUE = "OVERDUE"

class FinancingStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    FUNDED = "FUNDED"
    REPAID = "REPAID"
    REJECTED = "REJECTED"

class Payable(Base):
    """
    The bill the forwarder MUST PAY (e.g., to Maersk).
    This is what we will finance.
    """
    __tablename__ = "payables"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    payee_name = Column(String, default="Carrier") # "Maersk", "CMA CGM", etc.
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    booking = relationship("Booking", back_populates="payable")
    financing_request = relationship("FinancingRequest", back_populates="payable", uselist=False)

class Invoice(Base):
    """
    The bill the forwarder SENDS to their client.
    This is what we will collect on.
    """
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    booking = relationship("Booking", back_populates="invoice")
    client = relationship("Client", back_populates="invoices")

class FinancingRequest(Base):
    """
    The core "Loan" object.
    Links a Payable to our financing.
    """
    __tablename__ = "financing_requests"
    id = Column(Integer, primary_key=True, index=True)
    payable_id = Column(Integer, ForeignKey("payables.id"), unique=True)
    
    amount_requested = Column(Float)
    fee_percentage = Column(Float, default=2.5) # Our 2.5% fee
    fee_amount = Column(Float)
    total_repayment = Column(Float) # The invoice amount we collect
    
    status = Column(Enum(FinancingStatus), default=FinancingStatus.PENDING)
    requested_at = Column(DateTime)
    approved_at = Column(DateTime)
    funded_at = Column(DateTime)
    
    payable = relationship("Payable", back_populates="financing_request")
