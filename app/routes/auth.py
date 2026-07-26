

import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from app.validators import validate_email, validate_phone
from app import email_service

router = APIRouter()


def _log(db, user_id, action, details=""):
    db.add(models.TransactionLog(user_id=user_id, action=action, details=details))
    db.commit()


def _make_otp(db: Session, email: str) -> str:
    """6-digit OTP banao aur DB mein save karo."""
    code = str(random.randint(100000, 999999))
    db.query(models.OTPCode).filter(
        models.OTPCode.email == email.lower(),
        models.OTPCode.used == 0
    ).delete()
    db.add(models.OTPCode(
        email=email.lower(),
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    ))
    db.commit()
    return code


def _check_otp(db: Session, email: str, code: str) -> models.OTPCode:
    """OTP verify karo — galat ya expired pe exception."""
    otp = (
        db.query(models.OTPCode)
        .filter(
            models.OTPCode.email == email.lower(),
            models.OTPCode.code == code,
            models.OTPCode.used == 0,
        )
        .order_by(models.OTPCode.created_at.desc())
        .first()
    )
    if not otp:
        raise HTTPException(400, detail="❌ Wrong OTP — please check and try again")
    if otp.expires_at < datetime.utcnow():
        raise HTTPException(400, detail="❌ OTP expired — please request a new one")
    return otp


# ─── SIGNUP ──────────────────────────────────────────────────────
@router.post("/signup", response_model=schemas.UserOut, status_code=201)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validate_email(payload.email):
        raise HTTPException(400, detail="Invalid email — use real email like name@gmail.com")
    if payload.phone and not validate_phone(payload.phone):
        raise HTTPException(400, detail="Invalid phone — 10 digits, must start with 6-9")
    if db.query(models.User).filter(models.User.email == payload.email.lower()).first():
        raise HTTPException(400, detail="Email already registered — please login")
    if len(payload.name.strip()) < 2:
        raise HTTPException(400, detail="Name must be at least 2 characters")
    if len(payload.password) < 6:
        raise HTTPException(400, detail="Password must be at least 6 characters")

    user = models.User(
        name=payload.name.strip(),
        email=payload.email.lower().strip(),
        password_hash=hash_password(payload.password),
        phone=payload.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _log(db, user.user_id, "signup", user.email)
    return user


# ─── LOGIN ───────────────────────────────────────────────────────
@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.email.lower().strip()
    ).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, detail="Incorrect email or password")
    token = create_access_token(user.user_id)
    _log(db, user.user_id, "login", user.email)
    return {"access_token": token, "token_type": "bearer", "user": user}


# ─── ME ──────────────────────────────────────────────────────────
@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ═══════════════════════════════════════════════════════════════
# EMAIL VERIFICATION — Signup se pehle
# ═══════════════════════════════════════════════════════════════
class EmailRequest(BaseModel):
    email: str

class OTPConfirm(BaseModel):
    email: str
    code: str


@router.post("/send-verification")
def send_verification(payload: EmailRequest, db: Session = Depends(get_db)):
    """
    Signup se pehle user ke EMAIL pe OTP bhejo.
    - Email validate karo (format + fake check)
    - Already registered? Error do
    - OTP generate karo
    - SendGrid/SMTP se user ke email pe bhejo
    - Test mode mein screen pe bhi dikhao
    """
    email = payload.email.lower().strip()

    # Strict email validation — gnail.com jaisi fake emails block
    if not validate_email(email):
        raise HTTPException(400,
            detail="❌ Invalid email format — use real email like name@gmail.com")

    # Already registered check
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(400,
            detail="❌ Email already registered — please login instead")

    code = _make_otp(db, email)

    # Email bhejo USER KE APNE EMAIL PE
    email_sent = email_service.send_verification_email(email, code)

    return {
        "message": f"Verification code sent to {email}",
        "test_otp": code,          # Test mode — screen pe dikhao
        "email_sent": email_sent,
        "note": "TEST MODE — In production, remove test_otp from response"
    }


@router.post("/confirm-verification")
def confirm_verification(payload: OTPConfirm, db: Session = Depends(get_db)):
    """OTP confirm karo — sahi hone pe verified return karo."""
    otp = _check_otp(db, payload.email, payload.code)
    otp.used = 1
    db.commit()
    return {"verified": True, "email": payload.email}


# ═══════════════════════════════════════════════════════════════
# FORGOT PASSWORD — OTP via Email
# ═══════════════════════════════════════════════════════════════
class ForgotRequest(BaseModel):
    email: str

class ResetRequest(BaseModel):
    email: str
    code: str
    new_password: str


@router.post("/forgot-password")
def forgot_password(payload: ForgotRequest, db: Session = Depends(get_db)):
    """
    Password reset OTP bhejo USER KE REGISTERED EMAIL PE.
    - User exist karta hai? OTP bhejo
    - OTP screen pe bhi dikhao (test mode)
    """
    email = payload.email.lower().strip()
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        # Security: don't reveal if email exists
        return {
            "message": "If this email is registered, OTP has been sent.",
            "test_otp": None,
            "email_sent": False
        }

    code = _make_otp(db, email)

    # OTP USER KE APNE EMAIL PE BHEJO
    email_sent = email_service.send_otp_email(email, user.name, code)

    return {
        "message": f"OTP sent to {email}",
        "test_otp": code,           # Test mode — screen pe dikhao
        "email_sent": email_sent,
        "user_email": email,        # Confirm kaun sa email
    }


@router.post("/verify-otp")
def verify_otp(payload: OTPConfirm, db: Session = Depends(get_db)):
    """OTP verify karo — step 2."""
    _check_otp(db, payload.email, payload.code)
    return {"valid": True}


@router.post("/reset-password")
def reset_password(payload: ResetRequest, db: Session = Depends(get_db)):
    """OTP verify + password reset — step 3."""
    email = payload.email.lower().strip()
    otp = _check_otp(db, email, payload.code)

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    if len(payload.new_password) < 6:
        raise HTTPException(400, detail="Password must be at least 6 characters")

    user.password_hash = hash_password(payload.new_password)
    otp.used = 1
    db.commit()

    return {"message": "✅ Password reset successfully! Please login with your new password."}
