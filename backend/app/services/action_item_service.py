from sqlalchemy.orm import Session
from app.models.models import ActionItem
from app.schemas.schemas import ActionItemCreate, ActionItemUpdate
from fastapi import HTTPException

class ActionItemService:
    @staticmethod
    def create_action_item(db: Session, action_item: ActionItemCreate) -> ActionItem:
        """Create a new action item"""
        db_action_item = ActionItem(**action_item.dict())
        db.add(db_action_item)
        db.commit()
        db.refresh(db_action_item)
        return db_action_item
    
    @staticmethod
    def get_action_item(db: Session, action_item_id: int) -> ActionItem:
        """Get an action item by ID"""
        return db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
    
    @staticmethod
    def get_meeting_action_items(db: Session, meeting_id: int) -> list[ActionItem]:
        """Get all action items for a meeting"""
        return db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
    
    @staticmethod
    def update_action_item(db: Session, action_item_id: int, action_item: ActionItemUpdate) -> ActionItem:
        """Update an action item"""
        db_action_item = ActionItemService.get_action_item(db, action_item_id)
        if not db_action_item:
            raise HTTPException(status_code=404, detail="Action item not found")
        
        for key, value in action_item.dict(exclude_unset=True).items():
            setattr(db_action_item, key, value)
        
        db.commit()
        db.refresh(db_action_item)
        return db_action_item
    
    @staticmethod
    def delete_action_item(db: Session, action_item_id: int) -> bool:
        """Delete an action item"""
        db_action_item = ActionItemService.get_action_item(db, action_item_id)
        if not db_action_item:
            raise HTTPException(status_code=404, detail="Action item not found")
        
        db.delete(db_action_item)
        db.commit()
        return True 