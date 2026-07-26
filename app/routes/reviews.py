

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=schemas.ReviewOut, status_code=201)
def add_review(
    payload: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == payload.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    review = models.Review(
        user_id=current_user.user_id,
        hotel_id=payload.hotel_id,
        rating=payload.rating,
        comment=payload.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    # Hotel ki average rating recalculate karo
    avg = db.query(func.avg(models.Review.rating)).filter(
        models.Review.hotel_id == payload.hotel_id
    ).scalar()
    hotel.rating = round(avg, 1) if avg else 0.0
    db.commit()

    return review


@router.get("/hotel/{hotel_id}", response_model=List[schemas.ReviewOut])
def hotel_reviews(hotel_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Review)
        .filter(models.Review.hotel_id == hotel_id)
        .order_by(models.Review.created_at.desc())
        .all()
    )
