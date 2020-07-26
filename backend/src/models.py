from sqlalchemy import Integer, Column, String, Boolean

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, index=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=16), index=True)
    password = Column(String, index=True)

    @validates('username')
    def validate_username(self, key, value):
        assert value != ''
        assert value != None
        return value
