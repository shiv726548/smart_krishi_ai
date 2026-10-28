"""Authentication helpers for farmer and device APIs."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from typing import Any

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User

logger = logging.getLogger(__name__)

_configured_secret = os.getenv("JWT_SECRET_KEY")
if _configured_secret:
    _TOKEN_SECRET = _configured_secret.encode("utf-8")
    if len(_TOKEN_SECRET) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be at least 32 bytes")
else:
    # Keeps local demos usable without checking a secret into source control.
    # Tokens expire when this process restarts; deployments should set the secret.
    _TOKEN_SECRET = secrets.token_bytes(32)
    logger.warning(
        "JWT_SECRET_KEY is not configured; access tokens will be invalidated on restart."
    )

TOKEN_TTL_SECONDS = 60 * 60 * 12
_bearer = HTTPBearer(auto_error=False)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64url(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(user_id: int) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "iat": now, "exp": now + TOKEN_TTL_SECONDS}
    encoded_header = _b64url(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(_TOKEN_SECRET, signing_input, hashlib.sha256).digest()
    return f"{encoded_header}.{encoded_payload}.{_b64url(signature)}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        expected_signature = hmac.new(
            _TOKEN_SECRET, signing_input, hashlib.sha256
        ).digest()
        if not hmac.compare_digest(expected_signature, _unb64url(encoded_signature)):
            raise ValueError("Invalid token signature")
        header = json.loads(_unb64url(encoded_header))
        payload = json.loads(_unb64url(encoded_payload))
        if header != {"alg": "HS256", "typ": "JWT"}:
            raise ValueError("Unsupported token")
        if int(payload["exp"]) <= int(time.time()):
            raise ValueError("Expired token")
        user_id = int(payload["sub"])
        if user_id <= 0:
            raise ValueError("Invalid subject")
        return payload
    except (
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
        UnicodeDecodeError,
        binascii.Error,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt$16384$8$1${_b64url(salt)}${_b64url(derived)}"


def verify_password(password: str, stored_hash: str) -> bool:
    if stored_hash.startswith("scrypt$"):
        try:
            algorithm, n, r, p, salt, expected = stored_hash.split("$", 5)
            if algorithm != "scrypt":
                return False
            actual = hashlib.scrypt(
                password.encode("utf-8"),
                salt=_unb64url(salt),
                n=int(n),
                r=int(r),
                p=int(p),
                dklen=len(_unb64url(expected)),
            )
            return hmac.compare_digest(actual, _unb64url(expected))
        except (ValueError, TypeError):
            return False

    # Existing accounts used a plain SHA-256 digest. Accept it once at login,
    # then the auth route replaces it with scrypt.
    legacy_digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy_digest, stored_hash)


def is_legacy_password_hash(stored_hash: str) -> bool:
    return not stored_hash.startswith("scrypt$")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_farm_owner(user: User = Depends(get_current_user)) -> User:
    configured_owner = os.getenv("FARM_OWNER_USER_ID")
    if not configured_owner:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Farm-owner access is not configured for this deployment",
        )
    try:
        owner_id = int(configured_owner)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Farm-owner access is not configured correctly",
        )
    if user.id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this farm",
        )
    return user


def require_device_token(
    x_device_token: str | None = Header(default=None, alias="X-Device-Token"),
) -> None:
    configured_token = os.getenv("IOT_DEVICE_TOKEN")
    if not configured_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Device telemetry is not configured",
        )
    if not x_device_token or not hmac.compare_digest(x_device_token, configured_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device credentials",
        )
