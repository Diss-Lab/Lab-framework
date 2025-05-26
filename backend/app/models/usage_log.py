from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_type = Column(String(20), nullable=False)  # "equipment" or "material"
    resource_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # start_use/end_use/consume/maintenance
    quantity_used = Column(Numeric(10, 3))
    duration_minutes = Column(Integer)
    purpose = Column(String(200))
    notes = Column(Text)
    issues_reported = Column(Text)
    project_name = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    auto_recorded = Column(Boolean, default=False)
