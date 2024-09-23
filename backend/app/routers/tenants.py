from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserBase
from app.schemas.payment import PaymentCreate, PaymentResponse  # Import Pydantic schemas for payments
from app.auth import get_current_user
import app.crud as crud
from app.crud import create_message,get_messages_for_user
from app.schemas.message import MessageCreate, MessageResponse
import logging
from app.models.payment import Payment
from app.services.mpesa import initiate_stk_push

# Initialize logger
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile", response_model=UserBase)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

    
@router.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_message(db, current_user.id, message)

# New route to retrieve tenant's messages
@router.get("/messages/", response_model=list[MessageResponse])
def get_my_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = get_messages_for_user(db, current_user.id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return messages



# Endpoint to add a payment and trigger M-Pesa STK push
@router.post("/payments/", response_model=PaymentResponse)
async def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Get the current user
):
    logger.info(f"Creating payment: {payment}")
    try:
        db_payment = crud.create_payment(db=db, payment=payment, user_id=current_user.id)  # Pass user_id
        logger.info(f"Payment created with ID: {db_payment.id}")

        # Initiate STK push (you need to implement this function)
        stk_response = initiate_stk_push(payment.phone_number, payment.amount)
        logger.info(f"STK Push response: {stk_response}")

        if stk_response.get('ResponseCode') == '0':
            logger.info("STK Push successful")
            return db_payment
        else:
            logger.error(f"STK Push failed: {stk_response.get('ResponseDescription')}")
            raise HTTPException(status_code=400, detail="Failed to initiate M-Pesa payment")
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get user payment history
@router.get("/payments/{user_id}", response_model=list[PaymentResponse])
async def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    payments = crud.get_user_payments(db=db, user_id=user_id)
    if not payments:
        raise HTTPException(status_code=404, detail="No payment history found")
    return payments


# Endpoint to get all payments (for admin)
@router.get("/payments", response_model=list[PaymentResponse])
async def get_all_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    payments = crud.get_all_payments(db=db)
    return payments

# Callback endpoint for M-Pesa
@router.post("/mpesa/callback")
async def mpesa_callback(payload: dict, db: Session = Depends(get_db)):
    logger.info("M-Pesa Callback Received")
    logger.debug(f"Payload: {payload}")

    # Extract relevant details
    transaction_id = payload.get("Body", {}).get("stkCallback", {}).get("MerchantRequestID")
    result_code = payload.get("Body", {}).get("stkCallback", {}).get("ResultCode")
    
    logger.info(f"Processing payment with ID: {transaction_id} and result code: {result_code}")

    # Update payment status
    payment = crud.get_payment_by_transaction_id(db, transaction_id)
    
    if payment:
        logger.info(f"Found payment: {payment.id} with current status: {payment.status}")
        payment.status = "completed" if result_code == "0" else "failed"
        logger.info(f"Payment status updated to {payment.status}")
        
        db.commit()
        logger.info(f"Payment status saved: {payment.status}")
        return {"message": "Payment status updated"}
    else:
        logger.warning(f"Payment not found for ID: {transaction_id}")
        return {"message": "Payment not found"}, 404
