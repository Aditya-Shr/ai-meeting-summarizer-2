from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import ActionItem as ActionItemSchema, ActionItemCreate, ActionItemUpdate
from app.services.action_item_service import ActionItemService

router = APIRouter()

@router.post("/", response_model=ActionItemSchema)
async def create_action_item(
    action_item: ActionItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new action item"""
    return ActionItemService.create_action_item(db, action_item)

@router.get("/", response_model=List[ActionItemSchema])
async def get_action_items(
    meeting_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get action items, optionally filtered by meeting"""
    return ActionItemService.get_action_items(db, meeting_id=meeting_id, skip=skip, limit=limit)

@router.get("/{action_item_id}", response_model=ActionItemSchema)
async def get_action_item(
    action_item_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific action item by ID"""
    action_item = ActionItemService.get_action_item(db, action_item_id)
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return action_item

@router.put("/{action_item_id}", response_model=ActionItemSchema)
async def update_action_item(
    action_item_id: int,
    action_item_update: ActionItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an action item"""
    action_item = ActionItemService.update_action_item(db, action_item_id, action_item_update)
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return action_item

@router.delete("/{action_item_id}")
async def delete_action_item(
    action_item_id: int,
    db: Session = Depends(get_db)
):
    """Delete an action item"""
    success = ActionItemService.delete_action_item(db, action_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Action item not found")
    return {"message": "Action item deleted successfully"} 