from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StoreStatus(Base):
    __tablename__ = "store_status"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String)
    timestamp_utc = Column(DateTime)
    status = Column(String)  # 'active' or 'inactive'

class BusinessHours(Base):
    __tablename__ = "business_hours"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    start_time_local = Column(String)  # HH:MM:SS
    end_time_local = Column(String)

class Timezones(Base):
    __tablename__ = "timezones"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String)
    timezone_str = Column(String)  # e.g., America/Chicago
