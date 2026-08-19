"""
SK Enterprises | License Key Database Model
Inventor & Sole Architect: Sumeet Kumar
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from src_backend.app.database.base import Base

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String(500), unique=True, index=True, nullable=False)
    key_type = Column(String(50), nullable=False)  # SUPER_ADMIN_LIFETIME, USER_ANNUAL_365
    assigned_email = Column(String(255), index=True, nullable=False)
    assigned_name = Column(String(100), nullable=False)
    is_valid = Column(Boolean, default=True, nullable=False)
    is_lifetime = Column(Boolean, default=False, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    metadata_json = Column(Text, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "license_key": self.license_key,
            "key_type": self.key_type,
            "assigned_email": self.assigned_email,
            "assigned_name": self.assigned_name,
            "is_valid": self.is_valid,
            "is_lifetime": self.is_lifetime,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }
