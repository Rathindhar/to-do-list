
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    id: int
    title: str
    done: bool = False