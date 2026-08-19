"""
SK Enterprises | Security Audit Log Database Model
Inventor & Sole Architect: Sumeet Kumar
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from src_backend.app.database.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), index=True, nullable=False)
    severity = Column(String(50), default="INFO", index=True)  # INFO, WARNING, ERROR, CRITICAL
    actor = Column(String(255), default="SYSTEM")
    description = Column(Text, nullable=False)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "severity": self.severity,
            "actor": self.actor,
            "description": self.description,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
