"""
SK Enterprises | Chat Conversation & Message Database Models
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src_backend.app.database.base import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_email = Column(String(255), index=True, default="sumeet.admin@skenterprises.ai")
    persona = Column(String(50), default="SKAI")
    title = Column(String(200), default="Cognitive Session")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(50), nullable=False)  # USER or AI
    query = Column(Text, nullable=True)
    thought_process = Column(Text, nullable=True)
    response_content = Column(Text, nullable=False)
    voice_text = Column(Text, nullable=True)
    persona = Column(String(50), default="SKAI")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    conversation = relationship("Conversation", back_populates="messages")
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "query": self.query,
            "thought_process": self.thought_process,
            "response": self.response_content,
            "voice_text": self.voice_text,
            "persona": self.persona,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
