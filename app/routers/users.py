from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError




router = APIRouter(
    prefix="/user",
    tags=["User"]
)




@router.get("/me", response_model=schemas.User)
def get_current_user(me:schemas.User, current_user:int = Depends(oauth2.get_current_user), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id)

    return user





@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2PasswordRequestForm returns something like thad
        {"username": "example username,
         "password: "example password} " so we have to change user_credential.email in to
        user_credential.username"""
    """Also we have to change our testing way in postman (screen nr1) """
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")

    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id, "username": user.username})

    return {"access_token": access_token, "token_type": "Bearer"}



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    try:
        user.password = utils.hash_password(user.password)
        user = models.User(**user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)

        access_token = oauth2.create_access_token(data={"user_id": user.id, "username": user.username})
        
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.email} already exist. ")

    return JSONResponse({
        "data": jsonable_encoder(user),
        "access_token": access_token, 
        "token_type": "Bearer"
    })



@router.put('/update/data', status_code=status.HTTP_200_OK, response_model=schemas.User)
def update_user_data(update_user:schemas.UpdateUserData ,current_user:int = Depends(oauth2.get_current_user), db:Session=Depends(get_db,)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user{user.id}")

    try:
        user_query.update(update_user.dict(), synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail=f"User with email {update_user.email} already exist")

    return user
    




