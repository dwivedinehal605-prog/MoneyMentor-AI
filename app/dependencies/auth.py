from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.user_service import get_user_by_email
from app.utils.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user