"""
SK Enterprises | Cognitive Associative Memory Database Model
Inventor & Sole Architect: Sumeet Kumar
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from src_backend.app.database.base import Base

class MemoryItem(Base):
    __tablename__ = "memory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(200), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    category = Column(String(100), default="GENERAL", index=True)
    importance = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "content": self.content,
            "tags": [t.strip() for t in self.tags.split(",") if t.strip()] if self.tags else [],
            "category": self.category,
            "importance": self.importance,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
