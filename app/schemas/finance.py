# /app/schemas/finance.py
from pydantic import BaseModel
from datetime import datetime
from app.models.finance import FinancingStatus, PaymentStatus

class PayablePublic(BaseModel):
    id: int
    amount: float
    due_date: datetime
    status: PaymentStatus
    payee_name: str
    
    class Config:
        from_attributes = True

class InvoicePublic(BaseModel):
    id: int
    amount: float
    due_date: datetime
    status: PaymentStatus
    client_id: int
    
    class Config:
        from_attributes = True

class FinancingRequestPublic(BaseModel):
    id: int
    status: FinancingStatus
    amount_requested: float
    fee_amount: float
    total_repayment: float
    payable_id: int
    
    class Config:
        from_attributes = True
