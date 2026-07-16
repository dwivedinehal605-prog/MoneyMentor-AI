from app.utils.security import hash_password, verify_password
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.schemas.user import UserCreate

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        return None
    
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)   # We will hash this on Day 5
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except SQLAlchemyError:
        db.rollback()
        raise

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    print("=" * 40)
    print("Email:", email)
    print("User:", user)

    if user is None:
        print("User not found")
        return None

    print("Stored Hash:", user.password)

    result = verify_password(password, user.password)
    print("Password Match:", result)

    if not result:
        return None

    return user