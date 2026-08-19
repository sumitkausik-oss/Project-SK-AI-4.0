"""
SK Enterprises | User & Client Repository Layer
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src_backend.app.models.user import User

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, name: str, email: str, phone: Optional[str] = None, 
               location: Optional[str] = None, age: Optional[int] = None, 
               role: str = "USER", tier: str = "USER_ANNUAL_365") -> User:
        user = User(
            name=name,
            email=email,
            phone=phone,
            location=location,
            age=age,
            role=role,
            tier=tier,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_status(db: Session, email: str, is_active: bool) -> Optional[User]:
        user = UserRepository.get_by_email(db, email)
        if user:
            user.is_active = is_active
            db.commit()
            db.refresh(user)
        return user
