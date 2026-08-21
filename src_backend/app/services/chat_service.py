"""
SK Enterprises | Cognitive Chat & Multi-Persona Service
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from src_backend.app.core.config import settings
from src_backend.app.services.assistant_service import AssistantService

class ChatService:
    @staticmethod
    def process_query(db: Session, query: str, persona: str = "SKAI", language: str = "en-US", user_email: str = "sumeet.admin@skenterprises.ai") -> Dict[str, Any]:
        """Routes through the master AssistantService."""
        return AssistantService.process_command(
            db=db,
            query=query,
            persona=persona,
            language=language,
            user_email=user_email
        )
