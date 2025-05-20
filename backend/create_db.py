from app.core.database import engine
from app.models.models import Base
import os

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Create all tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
print("Uploads directory created successfully!") 