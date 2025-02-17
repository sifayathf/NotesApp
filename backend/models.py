from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NotesFolder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    files = relationship("NotesFile", back_populates="folder")

class NotesFile(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(Text)
    folder_id = Column(Integer, ForeignKey("folders.id"))

    folder = relationship("NotesFolder", back_populates="files")