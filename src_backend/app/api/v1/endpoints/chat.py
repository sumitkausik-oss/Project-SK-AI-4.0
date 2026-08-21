"""
SK Enterprises | SKAI Cognitive Assistant Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_backend.app.database.base import get_db
from src_backend.app.schemas.chat import ChatQueryRequest, ChatResponse
from src_backend.app.services.assistant_service import AssistantService

router = APIRouter(tags=["Cognitive Assistant"])

@router.post("/chat/process", response_model=ChatResponse, summary="Process Assistant Voice or Text Command")
@router.post("/chat", response_model=ChatResponse, summary="Process Command (Alias)")
def process_chat(req: ChatQueryRequest, db: Session = Depends(get_db)):
    return AssistantService.process_command(
        db=db,
        query=req.query,
        persona=req.persona,
        language=req.language,
        user_email=req.user_email or "sumeet.admin@skenterprises.ai"
    )
