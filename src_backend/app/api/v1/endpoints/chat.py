"""
SK Enterprises | Cognitive Chat Endpoints
Inventor & Sole Architect: Sumeet Kumar
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_backend.app.database.base import get_db
from src_backend.app.schemas.chat import ChatQueryRequest, ChatResponse
from src_backend.app.services.chat_service import ChatService

router = APIRouter(tags=["Cognitive Chat"])

@router.post("/chat/process", response_model=ChatResponse, summary="Process Cognitive Chat Query")
@router.post("/chat", response_model=ChatResponse, summary="Process Chat Query (Alias)")
def process_chat(req: ChatQueryRequest, db: Session = Depends(get_db)):
    return ChatService.process_query(
        db=db,
        query=req.query,
        persona=req.persona,
        language=req.language,
        user_email=req.user_email or "sumeet.admin@skenterprises.ai"
    )
