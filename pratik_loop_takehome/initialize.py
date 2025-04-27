import os
import sys
from sqlalchemy.orm import Session

# Add the current directory and parent directory to the path so we can import from modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine, SessionLocal
from db import models
from db.seed_data import seed_all_data

def init_db():
    """Initialize the database and seed data"""
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Seed data from CSV files
        seed_all_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing store monitoring system...")
    
    # Check if data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        print("Please make sure the data files are in the correct location")
        sys.exit(1)
    
    # Check if CSV files exist
    required_files = ["business_hours.csv", "store_status.csv", "timezones.csv"]
    missing_files = []
    
    for file in required_files:
        file_path = os.path.join(data_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: The following required data files are missing: {', '.join(missing_files)}")
        print("Please make sure all data files are in the data directory")
        sys.exit(1)
    
    # Initialize database
    init_db()
    
    print("Initialization complete!")
    print("You can now run the application with: python -m app.main")
