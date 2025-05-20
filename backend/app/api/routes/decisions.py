from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import Decision as DecisionSchema, DecisionCreate, DecisionUpdate
from app.services.decision_service import DecisionService

router = APIRouter()

@router.post("/", response_model=DecisionSchema)
async def create_decision(
    decision: DecisionCreate,
    db: Session = Depends(get_db)
):
    """Create a new decision"""
    return DecisionService.create_decision(db, decision)

@router.get("/", response_model=List[DecisionSchema])
async def get_decisions(
    meeting_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get decisions, optionally filtered by meeting"""
    return DecisionService.get_decisions(db, meeting_id=meeting_id, skip=skip, limit=limit)

@router.get("/{decision_id}", response_model=DecisionSchema)
async def get_decision(
    decision_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific decision by ID"""
    decision = DecisionService.get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@router.put("/{decision_id}", response_model=DecisionSchema)
async def update_decision(
    decision_id: int,
    decision_update: DecisionUpdate,
    db: Session = Depends(get_db)
):
    """Update a decision"""
    decision = DecisionService.update_decision(db, decision_id, decision_update)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@router.delete("/{decision_id}")
async def delete_decision(
    decision_id: int,
    db: Session = Depends(get_db)
):
    """Delete a decision"""
    success = DecisionService.delete_decision(db, decision_id)
    if not success:
        raise HTTPException(status_code=404, detail="Decision not found")
    return {"message": "Decision deleted successfully"} 