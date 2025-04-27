# check_data.py
from app.db.database import SessionLocal
from app.db.models import StoreStatus, BusinessHours, Timezones
from sqlalchemy import inspect

def check_inserted_data():
    db = SessionLocal()
    try:
        inspector = inspect(db.bind)
        print("✅ Tables in database:", inspector.get_table_names())

        print("\n🛒 First 5 rows in StoreStatus:")
        for row in db.query(StoreStatus).limit(5).all():
            print(f"Store ID: {row.store_id}, Status: {row.status}, Timestamp UTC: {row.timestamp_utc}")

        print("\n⏰ First 5 rows in BusinessHours:")
        for row in db.query(BusinessHours).limit(5).all():
            print(f"Store ID: {row.store_id}, Day: {row.day_of_week}, Start: {row.start_time_local}, End: {row.end_time_local}")

        print("\n🌎 First 5 rows in Timezones:")
        for row in db.query(Timezones).limit(5).all():
            print(f"Store ID: {row.store_id}, Timezone: {row.timezone_str}")

    finally:
        db.close()

if __name__ == "__main__":
    check_inserted_data()
