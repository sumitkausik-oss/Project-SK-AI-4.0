"""
SK Enterprises | SKAI Local Memory Management REST Endpoints
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src_backend.app.database.base import get_db
from src_backend.app.repositories.memory_repo import MemoryRepository, AuditRepository

router = APIRouter(prefix="/memory", tags=["Local Memory & Context"])

class StoreMemoryRequest(BaseModel):
    key: str = Field(..., min_length=1, example="Preferred Theme")
    content: str = Field(..., min_length=1, example="User prefers dark mode HUD")
    tags: Optional[List[str]] = Field(default=["preference", "user_context"])
    category: str = Field(default="GENERAL")
    importance: int = Field(default=1)

@router.get("", summary="List All Stored Durable Memories")
def list_memories(limit: int = Query(100), db: Session = Depends(get_db)):
    items = MemoryRepository.list_all(db, limit=limit)
    return {
        "count": len(items),
        "memories": [item.to_dict() for item in items]
    }

@router.post("", summary="Store or Update a Memory Fact")
def store_memory(req: StoreMemoryRequest, db: Session = Depends(get_db)):
    item = MemoryRepository.store_memory(
        db=db,
        key=req.key,
        content=req.content,
        tags=req.tags,
        category=req.category,
        importance=req.importance
    )
    AuditRepository.log_event(db, "STORE_MEMORY", f"Stored memory fact '{req.key}'", "INFO", "USER")
    return {
        "success": True,
        "message": f"Memory '{req.key}' stored successfully.",
        "memory": item.to_dict()
    }

@router.get("/search", summary="Associative Search Across Local Memories")
def search_memory(q: str = Query(..., description="Query phrase"), limit: int = Query(5), db: Session = Depends(get_db)):
    items = MemoryRepository.recall_associative(db, query=q, limit=limit)
    return {
        "query": q,
        "count": len(items),
        "matches": [item.to_dict() for item in items]
    }

@router.delete("/{memory_id}", summary="Delete a Memory Fact by ID or Key")
def delete_memory(memory_id: str, db: Session = Depends(get_db)):
    deleted = MemoryRepository.delete_memory(db, memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Memory '{memory_id}' not found.")
    AuditRepository.log_event(db, "DELETE_MEMORY", f"Deleted memory '{memory_id}'", "WARNING", "USER")
    return {
        "success": True,
        "message": f"Memory fact '{memory_id}' deleted successfully."
    }
