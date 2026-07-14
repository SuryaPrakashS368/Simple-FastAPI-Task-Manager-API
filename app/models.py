from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    status = Column(String, default="Pending")