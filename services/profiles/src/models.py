from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base, sync_engine


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    bio = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.now())



Base.metadata.create_all(bind=sync_engine)