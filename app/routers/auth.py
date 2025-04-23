from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, Oauth2
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.username).first()

    # user will have only username and password
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user.password, db_user.password):  # This is the correct hashed password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Password")

    # create a token
    access_token = Oauth2.create_access_tokens(data={"user_id": db_user.id, "email": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}