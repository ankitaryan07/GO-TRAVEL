

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_access_token
from app import models


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
