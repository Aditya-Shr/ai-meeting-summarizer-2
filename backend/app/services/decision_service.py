from sqlalchemy.orm import Session
from app.models.models import Decision
from app.schemas.schemas import DecisionCreate, DecisionUpdate
from fastapi import HTTPException

class DecisionService:
    @staticmethod
    def create_decision(db: Session, decision: DecisionCreate) -> Decision:
        """Create a new decision"""
        db_decision = Decision(**decision.dict())
        db.add(db_decision)
        db.commit()
        db.refresh(db_decision)
        return db_decision
    
    @staticmethod
    def get_decision(db: Session, decision_id: int) -> Decision:
        """Get a decision by ID"""
        return db.query(Decision).filter(Decision.id == decision_id).first()
    
    @staticmethod
    def get_meeting_decisions(db: Session, meeting_id: int) -> list[Decision]:
        """Get all decisions for a meeting"""
        return db.query(Decision).filter(Decision.meeting_id == meeting_id).all()
    
    @staticmethod
    def update_decision(db: Session, decision_id: int, decision: DecisionUpdate) -> Decision:
        """Update a decision"""
        db_decision = DecisionService.get_decision(db, decision_id)
        if not db_decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        for key, value in decision.dict(exclude_unset=True).items():
            setattr(db_decision, key, value)
        
        db.commit()
        db.refresh(db_decision)
        return db_decision
    
    @staticmethod
    def delete_decision(db: Session, decision_id: int) -> bool:
        """Delete a decision"""
        db_decision = DecisionService.get_decision(db, decision_id)
        if not db_decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        db.delete(db_decision)
        db.commit()
        return True 