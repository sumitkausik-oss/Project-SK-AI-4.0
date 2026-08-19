"""
SK Enterprises | User & Client Database Model
Inventor & Sole Architect: Sumeet Kumar
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from src_backend.app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    role = Column(String(50), default="USER", nullable=False)  # SUPER_ADMIN, ADMIN, USER
    tier = Column(String(50), default="USER_ANNUAL_365", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "age": self.age,
            "role": self.role,
            "tier": self.tier,
            "status": "ACTIVE" if self.is_active else "DISABLED",
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
