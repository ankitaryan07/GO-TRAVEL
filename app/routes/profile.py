

import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user
from app.security import hash_password, verify_password

router = APIRouter()

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    theme: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class PaymentMethodCreate(BaseModel):
    method_type: str           # "card" or "upi"
    label: Optional[str] = None
    # Card fields
    card_number: Optional[str] = None
    card_holder: Optional[str] = None
    card_expiry: Optional[str] = None
    # UPI field
    upi_id: Optional[str] = None
    # Legacy fallback
    value: Optional[str] = None


@router.get("/profile", response_model=schemas.UserOut)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=schemas.UserOut)
def update_profile(payload: ProfileUpdate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    if payload.email is not None:
        if not EMAIL_RE.match(payload.email):
            raise HTTPException(status_code=400, detail="Invalid email format")
        existing = db.query(models.User).filter(
            models.User.email == payload.email,
            models.User.user_id != current_user.user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = payload.email
    if payload.phone is not None and payload.phone != "":
        digits = re.sub(r"\D", "", payload.phone)
        if not PHONE_RE.match(digits):
            raise HTTPException(status_code=400, detail="Phone must be 10 digits starting with 6-9")
        current_user.phone = digits
    if payload.name is not None:
        if len(payload.name.strip()) < 2:
            raise HTTPException(status_code=400, detail="Name too short")
        current_user.name = payload.name.strip()
    if payload.photo_url is not None:
        current_user.photo_url = payload.photo_url
    if payload.theme in ("light", "dark"):
        current_user.theme = payload.theme
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/profile/password")
def change_password(payload: PasswordChange, db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password min 6 characters")
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@router.get("/profile/payment-methods")
def list_payment_methods(db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    methods = db.query(models.PaymentMethod).filter(
        models.PaymentMethod.user_id == current_user.user_id).all()
    result = []
    for m in methods:
        item = {
            "method_id": m.method_id,
            "method_type": m.method_type,
            "label": m.label,
            "masked_value": m.masked_value,
        }
        if m.method_type == "card":
            item["card_last4"] = m.masked_value[-4:] if m.masked_value else "****"
            item["card_holder"] = m.label or ""
        elif m.method_type == "upi":
            item["upi_id"] = m.masked_value or ""
        result.append(item)
    return result


@router.post("/profile/payment-methods")
def add_payment_method(payload: PaymentMethodCreate, db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    if payload.method_type == "card":
        # Accept card_number or legacy value
        raw = payload.card_number or payload.value or ""
        digits = re.sub(r"\D", "", raw)
        if len(digits) < 12:
            raise HTTPException(status_code=400, detail="Invalid card number — must be at least 12 digits")
        masked = "**** **** **** " + digits[-4:]
        holder = payload.card_holder or payload.label or "CARD HOLDER"
        label = holder.upper()
    elif payload.method_type == "upi":
        raw = payload.upi_id or payload.value or ""
        if "@" not in raw:
            raise HTTPException(status_code=400, detail="Invalid UPI ID — must contain @")
        masked = raw
        label = payload.label or "UPI"
    else:
        raise HTTPException(status_code=400, detail="Invalid method type — use 'card' or 'upi'")

    method = models.PaymentMethod(
        user_id=current_user.user_id,
        method_type=payload.method_type,
        label=label,
        masked_value=masked
    )
    db.add(method)
    db.commit()
    db.refresh(method)
    resp = {"method_id": method.method_id, "masked_value": masked, "label": label, "message": "Saved successfully!"}
    if payload.method_type == "card":
        resp["card_last4"] = digits[-4:]
        resp["card_holder"] = label
    else:
        resp["upi_id"] = masked
    return resp


@router.delete("/profile/payment-methods/{method_id}")
def delete_payment_method(method_id: int, db: Session = Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    method = db.query(models.PaymentMethod).filter(
        models.PaymentMethod.method_id == method_id,
        models.PaymentMethod.user_id == current_user.user_id).first()
    if not method:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(method)
    db.commit()
    return {"message": "Deleted"}
