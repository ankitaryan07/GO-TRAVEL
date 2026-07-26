

import json
import time
import hmac
import hashlib
import base64

import bcrypt

SECRET_KEY = "go-travel-secret-key-change-in-production-12345"
TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 30  # 30 days


# ---------- PASSWORD ----------
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ---------- JWT (self-made, no external library) ----------
def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_access_token(user_id: int) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "exp": int(time.time()) + TOKEN_EXPIRY_SECONDS}

    header_b64 = _b64encode(json.dumps(header).encode())
    payload_b64 = _b64encode(json.dumps(payload).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_access_token(token: str):
    
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")

        # Signature verify
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
        actual_sig = _b64decode(signature_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload = json.loads(_b64decode(payload_b64))

        # Expiry check
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        return None
