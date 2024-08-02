from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base, sync_engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now())


Base.metadata.create_all(bind=sync_engine)