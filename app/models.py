from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, BigInteger, Text, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime



class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    isbn = Column(BigInteger,nullable=False, unique=True)
    number_of_pages = Column(Integer,nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False,)
    author = relationship('Author', back_populates='books')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)

    