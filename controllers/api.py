from fastapi import APIRouter,Query, Depends, FastAPI,HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.database import SessionLocal, engine, Base,get_db
from models.userModel import User
from schemas.userSchema import UserCreate,UserUpdate,Userr
from email_validator import validate_email, EmailNotValidError
from typing import List,Optional
Base.metadata.create_all(bind=engine)
router = APIRouter()
@router.get("/")
async def hello():
    return JSONResponse(content={"message": "Hello, World!"})
# CREATE USER
@router.post("/users/",response_model=Userr)
def create_user( user: UserCreate,db: Session = Depends(get_db)):
    try:
        validEmail = validate_email(user.email, check_deliverability=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email is not valid")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(**user.dict())
    db.add(db_user) 
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user
# GET All USERS
@router.get("/users/",response_model=List[Userr])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [Userr.from_orm(user) for user in users]
# GET ONE USER BY ID
@router.get("/users/{user_id}",response_model=Userr)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# UPDATE USER BY ID
@router.patch("/users/{user_id}",response_model=Userr)
def update_user(user_id: int,user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
# DELETE USER BY ID
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
# FILTER PROFILES
@router.get("/filter/",response_model=List[Userr])
def filter_users( 
    age: Optional[int] = None,
    gender: Optional[str] = None,
    occupation: Optional[str] = None,
    city: Optional[str] = None,
    # interests: Optional[list[str]] = None,
    interests: Optional[list[str]] = Query(None),
    skip: int = 0, limit: int = 10, 
    db: Session = Depends(get_db)):
    query = db.query(User)
    if age is not None:
        query = query.filter(User.age == age)
    if gender is not None:
        query = query.filter(User.gender == gender)
    if occupation is not None:
        query = query.filter(User.occupation == occupation)
    if city is not None:
        query = query.filter(User.city == city)
    users = query.offset(skip).limit(limit).all()
    if interests:
        users = [user for user in users if any(interest in user.interests for interest in interests)]
    return [Userr.from_orm(user) for user in users]