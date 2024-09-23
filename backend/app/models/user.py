
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from enum import Enum as PyEnum
from app.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Role(str, PyEnum):
    tenant = "tenant"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    def verify_password(self, password: str) -> bool:
        """Verify the provided password."""
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash the provided password."""
        return pwd_context.hash(password)
