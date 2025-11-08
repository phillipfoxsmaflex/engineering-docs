

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from database import Base
from models.user import User
from models.document import Document, DocumentVersion
from models.folder import Folder
from core.security import get_password_hash

DATABASE_URL = "sqlite:///./test.db"

def init_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Establish relationships to avoid circular imports
    User.documents = relationship("Document", order_by=Document.id, back_populates="creator")

def create_admin_user_if_not_exists():
    """Create an admin user if no users exist in the database."""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        # Check if any users exist
        user_count = session.query(User).count()
        if user_count == 0:
            print("No users found. Creating admin user...")

            # Create admin user
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("password123"),
                is_admin=True
            )
            session.add(admin_user)
            session.commit()
            print("Admin user created successfully!")
        else:
            print(f"{user_count} users found. Skipping admin creation.")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    create_admin_user_if_not_exists()
    print("Database initialized successfully!")

