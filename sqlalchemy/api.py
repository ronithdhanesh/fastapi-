from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from typing import List

app = FastAPI(title="FASTAPI-SQLALCHEMY")

engine = create_engine("sqlite:///users.db",connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)

class UserCreate(BaseModel):
    name:str
    email:str
    role:str

class UserResponse(BaseModel):
    id: int
    name:str
    email: str
    role: str

    class Config:
        from_attributes = True






Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message":"this is first endpoint go ahead for CRUD"}\


@app.get("/users")
def get_users(db: Session = Depends((get_db))):
    users = db.query(User).all()
    return users

@app.get('/users/{user_id}')
def get_user(user_id: int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return HTTPException(status_code=400, detail="User already exists ")
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id:int,user: UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        return HTTPException(status_code=404, detail="user not found")

    for field, value in user.dict().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}