from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, default=None)
    chat_id = Column(String)
    url = Column(String)
    screenshot = Column(String, default=None)
    date = Column(DateTime(timezone=True))
