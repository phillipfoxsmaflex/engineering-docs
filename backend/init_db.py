

import os
import psycopg2
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from database import Base
from models.user import User
from models.document import Document, DocumentVersion
from models.folder import Folder
from core.security import get_password_hash

# Use environment variables for database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

def create_db_and_user():
    """Create the PostgreSQL user and database if they don't exist."""
    try:
        # Extract credentials from DATABASE_URL
        import re
        match = re.match(r'postgresql:\/\/(.*):(.*)@(.*):(\d+)\/(.*)', DATABASE_URL)
        if not match:
            print("Could not parse DATABASE_URL. Skipping user creation.")
            return

        db_user, db_password, db_host, db_port, db_name = match.groups()

        # Connect to postgres (not a specific database)
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        if not cursor.fetchone():
            print(f"Creating database {db_name}...")
            cursor.execute(f"CREATE DATABASE {db_name}")
        else:
            print(f"Database {db_name} already exists.")

        # Close the connection and reconnect to the specific database
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")


def init_db():
    engine = create_engine(DATABASE_URL)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Establish relationships to avoid circular imports
    User.documents = relationship("Document", order_by=Document.id, back_populates="creator")

def create_admin_user_if_not_exists():
    """Create an admin user if no users exist in the database."""
    engine = create_engine(DATABASE_URL)
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
    # First create the database and user if needed
    create_db_and_user()

    # Then initialize the database schema and create admin user
    init_db()
    create_admin_user_if_not_exists()
    print("Database initialized successfully!")

