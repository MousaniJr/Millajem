"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from app.auth import (
    Token,
    LoginRequest,
    User,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Login endpoint

    Default credentials:
    - Username: admin
    - Password: millajem2026

    Can be changed via environment variables:
    - ADMIN_USERNAME
    - ADMIN_PASSWORD
    """
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.post("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verify if token is valid"""
    return {"valid": True, "username": current_user.username}
