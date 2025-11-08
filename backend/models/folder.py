


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)

    parent = relationship("Folder", remote_side=[id], back_populates="children")
    children = relationship("Folder", back_populates="parent")
    documents = relationship("Document", back_populates="folder")

