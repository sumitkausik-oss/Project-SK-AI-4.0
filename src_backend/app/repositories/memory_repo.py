"""
SK Enterprises | Memory, Chat & Audit Repository Layers
Inventor & Sole Architect: Sumeet Kumar
"""
import re
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from src_backend.app.models.memory import MemoryItem
from src_backend.app.models.chat import Conversation, Message
from src_backend.app.models.audit import AuditLog

class MemoryRepository:
    @staticmethod
    def store_memory(db: Session, key: str, content: str, tags: Optional[List[str]] = None, category: str = "GENERAL", importance: int = 1) -> MemoryItem:
        tags_str = ",".join(tags) if tags else ""
        item = db.query(MemoryItem).filter(MemoryItem.key == key).first()
        if item:
            item.content = content
            item.tags = tags_str
            item.category = category
            item.importance = importance
        else:
            item = MemoryItem(key=key, content=content, tags=tags_str, category=category, importance=importance)
            db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_memory(db: Session, key: str) -> Optional[MemoryItem]:
        return db.query(MemoryItem).filter(MemoryItem.key == key).first()

    @staticmethod
    def recall_associative(db: Session, query: str, limit: int = 5) -> List[MemoryItem]:
        words = set(re.findall(r'\b\w+\b', query.lower()))
        all_items = db.query(MemoryItem).all()
        scored = []
        for item in all_items:
            item_words = set(re.findall(r'\b\w+\b', (item.key + " " + (item.tags or "")).lower()))
            overlap = len(words.intersection(item_words))
            if overlap > 0:
                scored.append((overlap, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:limit]]

    @staticmethod
    def list_all(db: Session, limit: int = 100) -> List[MemoryItem]:
        return db.query(MemoryItem).order_by(MemoryItem.importance.desc(), MemoryItem.updated_at.desc()).limit(limit).all()

class ChatRepository:
    @staticmethod
    def get_or_create_conversation(db: Session, session_id: str, user_email: str = "sumeet.admin@skenterprises.ai", persona: str = "JARVIS") -> Conversation:
        conv = db.query(Conversation).filter(Conversation.session_id == session_id).first()
        if not conv:
            conv = Conversation(session_id=session_id, user_email=user_email, persona=persona)
            db.add(conv)
            db.commit()
            db.refresh(conv)
        return conv

    @staticmethod
    def add_message(db: Session, conversation_id: int, sender: str, response_content: str, query: Optional[str] = None, thought_process: Optional[str] = None, voice_text: Optional[str] = None, persona: str = "JARVIS") -> Message:
        msg = Message(
            conversation_id=conversation_id,
            sender=sender,
            query=query,
            thought_process=thought_process,
            response_content=response_content,
            voice_text=voice_text,
            persona=persona
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_recent_messages(db: Session, limit: int = 20) -> List[Message]:
        return db.query(Message).order_by(Message.timestamp.desc()).limit(limit).all()

class AuditRepository:
    @staticmethod
    def log_event(db: Session, event_type: str, description: str, severity: str = "INFO", actor: str = "SYSTEM", ip_address: str = "127.0.0.1") -> AuditLog:
        audit = AuditLog(
            event_type=event_type,
            description=description,
            severity=severity,
            actor=actor,
            ip_address=ip_address
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit

    @staticmethod
    def get_recent(db: Session, limit: int = 50) -> List[AuditLog]:
        return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
