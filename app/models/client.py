# /app/models/client.py
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base

class Client(Base):
    """
    A client (shipper) of the freight forwarder.
    Belongs to an Organization.
    """
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="clients")

    invoices = relationship("Invoice", back_populates="client")
