from pydantic import BaseModel
from datetime import datetime

# Schema for creating a payment
class PaymentCreate(BaseModel):
    phone_number: str  # User's phone number
    amount: float      # Amount the user wants to pay
    house_number: str  # Reference to the user's house number

# Schema for returning payment info
class PaymentResponse(BaseModel):
    id: int
    phone_number: str
    amount: float
    house_number: str
    status: str
    created_at: datetime  # Include created_at in the response

    class Config:
        from_attributes = True  # Use from_attributes instead of orm_mode
