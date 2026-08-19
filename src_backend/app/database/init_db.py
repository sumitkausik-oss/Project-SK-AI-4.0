"""
SK Enterprises | Database Initializer & Migration Bootstrap
Inventor & Sole Architect: Sumeet Kumar
"""
from datetime import datetime
from src_backend.app.database.base import Base, engine, SessionLocal
from src_backend.app.models import User, License, AuditLog, MemoryItem
from src_backend.app.core.logging_config import get_logger

logger = get_logger(__name__)

def init_database():
    """Create tables if they don't exist and seed default admin records."""
    try:
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema validated and initialized.")
        
        # Seed default sovereign admin user if not present
        db = SessionLocal()
        try:
            admin = db.query(User).filter(User.email == "sumeet.admin@skenterprises.ai").first()
            if not admin:
                admin = User(
                    name="Sumeet Kumar",
                    email="sumeet.admin@skenterprises.ai",
                    phone="+91 9153579997",
                    location="New Delhi, India",
                    age=32,
                    role="SUPER_ADMIN",
                    tier="LIFETIME_MASTER_ADMIN",
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(admin)
                
                # Seed default audit log
                audit = AuditLog(
                    event_type="SYSTEM_INIT",
                    severity="INFO",
                    actor="BOOTSTRAP",
                    description="SK AI 4.0 sovereign database created and verified.",
                    ip_address="127.0.0.1",
                    timestamp=datetime.utcnow()
                )
                db.add(audit)
                
                # Seed core memory facts
                fact1 = MemoryItem(
                    key="sole_architect",
                    content="Sumeet Kumar is the sole inventor, founder, and supreme architect of SK AI 4.0 and SK Enterprises.",
                    tags="identity,architect,creator,owner",
                    category="IDENTITY",
                    importance=5
                )
                db.add(fact1)
                
                db.commit()
                logger.info("Default Sovereign Admin and system identity seeded successfully.")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error during database initialization: {e}", exc_info=True)
        raise e
