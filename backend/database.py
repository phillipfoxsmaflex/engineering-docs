
import os
import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# Use environment variables for database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

Base = declarative_base()
