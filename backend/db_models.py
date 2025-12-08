# SQLAlchemy database models
from sqlalchemy import Column, String, Integer, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone

Base = declarative_base()


class JobModel(Base):
    """SQLAlchemy model for jobs table"""
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, index=True)
    num_images = Column(Integer, nullable=False)
    animal = Column(String, nullable=True)
    image_urls = Column(ARRAY(String), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Job(id={self.id}, status={self.status}, animal={self.animal})>"
