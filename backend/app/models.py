from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class RandomNumber(Base):
    __tablename__ = 'random_numbers'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class CsvFileVersion(Base):
    __tablename__ = 'csv_file_versions'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
