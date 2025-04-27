# app/scripts/seed_data.py

import pandas as pd
from app.db.database import SessionLocal, engine
from app.db.models import Base, StoreStatus, BusinessHours, Timezones
from datetime import datetime

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def load_store_status():
    db = SessionLocal()
    try:
        df = pd.read_csv('app/data/store_status.csv')
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
        store_statuses = df.to_dict(orient="records")
        db.bulk_insert_mappings(StoreStatus, store_statuses)
        db.commit()
        print("✅ store_status seeded")
    finally:
        db.close()

def load_business_hours():
    db = SessionLocal()
    try:
        df = pd.read_csv('app/data/business_hours.csv')  # Corrected file name
        df = df.rename(columns={"dayOfWeek": "day_of_week"})  # ensure correct field
        business_hours = df.to_dict(orient="records")
        db.bulk_insert_mappings(BusinessHours, business_hours)
        db.commit()
        print("✅ business_hours seeded")
    finally:
        db.close()

def load_timezones():
    db = SessionLocal()
    try:
        df = pd.read_csv('app/data/timezones.csv')
        timezones = df.to_dict(orient="records")
        db.bulk_insert_mappings(Timezones, timezones)
        db.commit()
        print("✅ timezones seeded")
    finally:
        db.close()

if __name__ == "__main__":
    load_store_status()
    load_business_hours()
    load_timezones()
    print("\n🎉 All data seeded successfully!")
