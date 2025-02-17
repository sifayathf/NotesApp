from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  # Add this import
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request validation
class FolderCreate(BaseModel):
    name: str

class FileCreate(BaseModel):
    name: str
    content: str
    folder_id: int

# API endpoints
@app.post("/folders/")
def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    db_folder = models.NotesFolder(name=folder.name)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

@app.get("/folders/")
def read_folders(db: Session = Depends(get_db)):
    return db.query(models.NotesFolder).all()

@app.post("/files/")
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    db_file = models.NotesFile(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@app.get("/files/")
def read_files(folder_id: int, db: Session = Depends(get_db)):
    return db.query(models.NotesFile).filter(models.NotesFile.folder_id == folder_id).all()

@app.get("/files/{file_id}")
def read_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.NotesFile).filter(models.NotesFile.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file

# Serve the index.html file at the root URL
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")
