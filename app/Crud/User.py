from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas
from ..utils import hash_password
from ..utils import verify_password

# -------------------------
# Get User by Email
# -------------------------

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


# -------------------------
# Create User
# -------------------------

def create_user(db: Session, user: schemas.UserCreate):

    hashed_pwd = hash_password(user.password)

    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role

    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# -------------------------
# Authenticate User
# -------------------------

def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user
