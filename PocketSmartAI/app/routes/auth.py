from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db

from app.models.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)

from app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserOut,
)
def register(
    data: RegisterRequest,
):
    email = data.email.lower().strip()
    name = data.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required",
        )

    with get_db() as db:

        existing = db.execute(
            """
            SELECT 1
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered",
            )

        cursor = db.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(data.password),
            ),
        )

        return {
            "id": cursor.lastrowid,
            "name": name,
            "email": email,
        }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
):
    email = data.email.lower().strip()

    with get_db() as db:

        row = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if (
        not row
        or not verify_password(
            data.password,
            row["password_hash"],
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(row["id"]),
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserOut,
)
def me(
    user=Depends(get_current_user),
):
    return user