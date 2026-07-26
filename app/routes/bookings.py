

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == payload.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    nights = (payload.check_out - payload.check_in).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    total = hotel.price_per_night * nights
    booking = models.Booking(
        user_id=current_user.user_id, hotel_id=payload.hotel_id, trip_id=payload.trip_id,
        check_in=payload.check_in, check_out=payload.check_out,
        total_amount=total, status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    db.add(models.TransactionLog(user_id=current_user.user_id, action="booking_created",
                                 details=f"{hotel.name}, {nights} nights, INR {total}"))
    db.commit()
    return booking


@router.get("", response_model=List[schemas.BookingOut])
def my_bookings(db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    return (db.query(models.Booking)
            .filter(models.Booking.user_id == current_user.user_id)
            .order_by(models.Booking.created_at.desc()).all())


@router.post("/{booking_id}/cancel", response_model=schemas.BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    booking = (db.query(models.Booking)
               .filter(models.Booking.booking_id == booking_id,
                       models.Booking.user_id == current_user.user_id).first())
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    booking = (db.query(models.Booking)
               .filter(models.Booking.booking_id == booking_id,
                       models.Booking.user_id == current_user.user_id).first())
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
