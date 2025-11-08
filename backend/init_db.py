

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship
from database import Base
from models.user import User
from models.document import Document, DocumentVersion
from models.folder import Folder

DATABASE_URL = "sqlite:///./test.db"

def init_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Establish relationships to avoid circular imports
    User.documents = relationship("Document", order_by=Document.id, back_populates="creator")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

