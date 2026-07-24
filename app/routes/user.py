from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..oauth2 import create_access_token
from ..oauth2 import get_current_user
from .. import models
from ..database import get_db
from .. import schemas
from app.Crud import User
from app.Crud.activity import create_activity_log

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=schemas.UserResponse
)
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = User.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return User.create_user(
        db,
        user
    )


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = User.authenticate_user(
        db,
        user_credentials.username,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    access_token = create_access_token(
        data={
            "id": user.id
        }
    )
    
    create_activity_log(
    db=db,
    user_id=user.id,
    action="LOGIN",
    entity_type="User",
    entity_id=user.id,
    description=f"{user.full_name} logged into the system."
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_me(
    current_user: models.User = Depends(
        get_current_user
    )
):

    return current_user