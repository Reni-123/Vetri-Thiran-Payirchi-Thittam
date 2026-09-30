from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.db import get_db


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


bearer = HTTPBearer(
    auto_error=False
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed: str,
) -> bool:
    return pwd_context.verify(
        password,
        hashed,
    )


def create_access_token(
    user_id: int,
) -> str:

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer
    ),
):

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        user_id = int(payload["sub"])

    except (
        JWTError,
        KeyError,
        ValueError,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    with get_db() as db:

        row = db.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if not row:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return dict(row)