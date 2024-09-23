from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base  
from app.models.user import User, Role
from app.models.payment import Payment
from app.models.message import Message 

# Create all tables in the database
Base.metadata.create_all(bind=engine)
    
def seed_data(db: Session):
    # Seed users
    if db.query(User).count() > 0:
        print("Database already seeded with users.")
        return

    tenant_user = User(
        username="tenant_user",
        email="tenant@example.com",
        hashed_password=User.hash_password("password123"),
        role=Role.tenant
    )

    admin_user = User(
        username="admin_user",
        email="admin@example.com",
        hashed_password=User.hash_password("password123"),
        role=Role.admin
    )

    # Add users to the session and commit to the database
    db.add_all([tenant_user, admin_user])
    db.commit()
    
    print("Database seeded with initial users.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
