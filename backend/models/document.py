

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    document_number = Column(String, unique=True, index=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Entwurf")  # Entwurf, In Prüfung, Genehmigt, Abgelehnt

    creator = relationship("User", back_populates="documents")
    folder = relationship("Folder", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_number = Column(String, nullable=False)  # e.g., v1.0, v1.1
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    comment = Column(String, nullable=True)

    document = relationship("Document", back_populates="versions")

