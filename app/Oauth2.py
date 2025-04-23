from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret_key
# algorithm 
# expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_tokens(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        user_id: int = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id, email=email)
    except JWTError:
        raise credentials_exception

    return token_data

    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token=token, credentials_exception=credential_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user