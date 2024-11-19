from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TimeEntries(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key = True)
    description = Column(String)
    duration = Column(Integer)

class Connect():
    def create_connection():
        engine = create_engine("postgresql://postgres@localhost:5432/postgres")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session