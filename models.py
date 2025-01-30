from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
Base = declarative_base()

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False)

# Create the SQLite database connection
DATABASE_URL = "sqlite:///alerts.db"
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

class Message(BaseModel):
    message: str