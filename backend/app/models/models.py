from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    date = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
    participants = Column(Text, nullable=True)  # Store as JSON string
    status = Column(String, nullable=True)
    audio_file_path = Column(String)
    transcript = Column(Text)
    summary = Column(Text)
    calendar_event_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    action_items = relationship("ActionItem", back_populates="meeting")
    decisions = relationship("Decision", back_populates="meeting")

class ActionItem(Base):
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    assignee = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    meeting = relationship("Meeting", back_populates="action_items")

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    decision_maker = Column(String(255), nullable=False)
    rationale = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    meeting = relationship("Meeting", back_populates="decisions") 