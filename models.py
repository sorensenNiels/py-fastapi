""" Models """

from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Todo(Base):
    """This is a Todo class used for representing a Todo item in the database."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    complete = Column(Boolean, default=False)


# schemas?
