

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter()


def _check_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/admin/stats")
def stats(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    payments = db.query(models.Payment).all()
    bookings = db.query(models.Booking).all()
    return {
        "total_users": db.query(models.User).filter(models.User.is_admin == 0).count(),
        "total_bookings": len(bookings),
        "confirmed_bookings": len([b for b in bookings if b.status == "confirmed"]),
        "total_revenue": sum(p.amount for p in payments if p.status == "paid"),
        "total_hotels": db.query(models.Hotel).count(),
        "total_trips": db.query(models.Trip).count(),
    }


@router.get("/admin/users")
def all_users(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return [{
        "user_id": u.user_id, "name": u.name, "email": u.email,
        "phone": u.phone or "-", "password": "********",  # masked for privacy
        "is_admin": u.is_admin, "trips": len(u.trips), "bookings": len(u.bookings),
        "created_at": str(u.created_at),
    } for u in users]


@router.get("/admin/bookings")
def all_bookings(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    bookings = db.query(models.Booking).order_by(models.Booking.created_at.desc()).all()
    return [{
        "booking_id": b.booking_id, "user_name": b.user.name, "user_email": b.user.email,
        "user_phone": b.user.phone or "-", "hotel_name": b.hotel.name, "city": b.hotel.city,
        "check_in": str(b.check_in.date()), "check_out": str(b.check_out.date()),
        "amount": b.total_amount, "status": b.status,
        "payment_status": b.payment.status if b.payment else "no_payment",
        "created_at": str(b.created_at),
    } for b in bookings]


@router.get("/admin/payments")
def all_payments(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    payments = db.query(models.Payment).order_by(models.Payment.payment_id.desc()).all()
    return [{
        "payment_id": p.payment_id, "booking_id": p.booking_id,
        "user_name": p.booking.user.name, "user_email": p.booking.user.email,
        "amount": p.amount, "method": p.payment_method, "status": p.status,
        "txn_id": p.txn_id or "-", "paid_at": str(p.paid_at) if p.paid_at else "-",
    } for p in payments]


@router.get("/admin/trips")
def all_trips(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    trips = db.query(models.Trip).order_by(models.Trip.created_at.asc()).all()
    return [{
        "trip_id": t.trip_id, "user_name": t.user.name, "user_email": t.user.email,
        "destination": t.destination, "budget": t.budget, "days": t.duration_days,
        "status": t.status, "created_at": str(t.created_at),
    } for t in trips]


@router.get("/admin/hotels")
def all_hotels(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    hotels = db.query(models.Hotel).order_by(models.Hotel.city).all()
    return [{
        "hotel_id": h.hotel_id, "name": h.name, "state": h.state, "city": h.city,
        "price_per_night": h.price_per_night, "rating": h.rating,
        "amenities": h.amenities or "-",
    } for h in hotels]


@router.get("/admin/reviews")
def all_reviews(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    reviews = db.query(models.Review).order_by(models.Review.created_at.desc()).all()
    return [{
        "review_id": r.review_id, "user_name": r.user.name, "hotel_name": r.hotel.name,
        "rating": r.rating, "comment": r.comment or "-", "created_at": str(r.created_at),
    } for r in reviews]


@router.get("/admin/logs")
def all_logs(db: Session = Depends(get_db), admin: models.User = Depends(_check_admin)):
    logs = db.query(models.TransactionLog).order_by(
        models.TransactionLog.timestamp.desc()).limit(200).all()
    return [{
        "log_id": l.log_id, "user_id": l.user_id or "-", "action": l.action,
        "details": l.details or "-", "timestamp": str(l.timestamp),
    } for l in logs]
