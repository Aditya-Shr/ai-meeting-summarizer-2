from app.core.database import recreate_tables
from app.models.models import Base
 
if __name__ == "__main__":
    print("Recreating database tables...")
    recreate_tables()
    print("Database tables recreated successfully!") 