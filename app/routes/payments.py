
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user
from app import payment_service, email_service

router = APIRouter()


@router.post("/create", response_model=schemas.PaymentOrderOut)
def create_payment(
    payload: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    

    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == payload.booking_id,
        models.Booking.user_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    
    order = payment_service.create_order(
        amount_inr=booking.total_amount,
        receipt=f"booking_{booking.booking_id}"
    )

    # save Payment record to db 
    payment = models.Payment(
        booking_id=booking.booking_id,
        amount=booking.total_amount,
        payment_method="razorpay" if not order["mock"] else "mock",
        txn_id=order["order_id"],
        status="created",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.payment_id,
        "order_id":   order["order_id"],
        "amount":     booking.total_amount,
        "currency":   "INR",
        "key_id":     order["key_id"],
        "mock":       order["mock"],
    }


@router.post("/verify", response_model=schemas.BookingOut)
def verify_payment(
    payload: schemas.PaymentVerify,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
   
    # find Payment record
    payment = db.query(models.Payment).filter(
        models.Payment.payment_id == payload.payment_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    
    is_valid = payment_service.verify_payment(
        order_id=payload.order_id,
        payment_id=payload.razorpay_payment_id,
        signature=payload.razorpay_signature
    )

    if not is_valid:
        payment.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail="Payment verification failed")

    # Payment successful -  update records
    payment.status = "paid"
    payment.txn_id = payload.razorpay_payment_id
    payment.paid_at = datetime.utcnow()

    # Booking confirmed
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == payment.booking_id
    ).first()
    booking.status = "confirmed"

    # save in Activity log 
    db.add(models.TransactionLog(
        user_id=current_user.user_id,
        action="payment_done",
        details=f"Booking #{booking.booking_id} confirmed, Amount: INR {payment.amount}"
    ))
    db.commit()
    db.refresh(booking)

    # send email to user for Booking confirmation 
    hotel = db.query(models.Hotel).filter(
        models.Hotel.hotel_id == booking.hotel_id
    ).first()

    email_service.send_booking_confirmation(
        to_email=current_user.email,
        name=current_user.name,
        hotel_name=hotel.name,
        check_in=str(booking.check_in.date()),
        check_out=str(booking.check_out.date()),
        amount=booking.total_amount,
    )

    return booking
