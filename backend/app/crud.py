from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageReply
from app.models.property import Property


# Create a new payment entry
def create_payment(db: Session, payment: PaymentCreate, user_id: int) -> Payment:
    db_payment = Payment(
        phone_number=payment.phone_number,
        amount=payment.amount,
        house_number=payment.house_number,
        status="pending",  # Initialize status as pending
        created_by_id=user_id  # Set the created_by_id field
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# Get payment history for a specific user 
def get_user_payments(db: Session, user_id: int):
    return db.query(Payment).filter(Payment.created_by_id == user_id).all()

# Get all payments (for admin)
def get_all_payments(db: Session):
    return db.query(Payment).all()

# Get a payment by transaction ID
def get_payment_by_transaction_id(db: Session, transaction_id: str):
    return db.query(Payment).filter(Payment.transaction_id == transaction_id).first()



def create_message(db: Session, user_id: int, message: MessageCreate):
    db_message = Message(
        content=message.content,
        created_by_id=user_id,
        urgency=message.urgency
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_for_user(db: Session, user_id: int):
    return db.query(Message).filter(Message.created_by_id == user_id).all()

def get_messages_for_admin(db: Session):
    return db.query(Message).all()

def reply_to_message(db: Session, message_id: int, reply: MessageReply):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db_message.reply = reply.reply
        db.commit()
        db.refresh(db_message)
    return db_message



def create_property(db: Session, name: str, location: str, number_of_houses: int, description: str):
    db_property = Property(name=name, location=location, number_of_houses=number_of_houses, description=description)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def get_properties(db: Session):
    return db.query(Property).all()
