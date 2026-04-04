from fastapi import Header, HTTPException

from app.core.config import settings


def check_secret_key(x_secret_key: str = Header(None)):
    if not x_secret_key:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    if x_secret_key != settings.x_secret_key:
        raise HTTPException(
            status_code=401, detail="Unauthorized access wrong secret key."
        )
    return True
