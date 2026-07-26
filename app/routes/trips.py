

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user
from app.ai_service import generate_trip_plan
from app import email_service

router = APIRouter()


@router.post("", response_model=schemas.TripOut, status_code=201)
def create_trip(
    payload: schemas.TripCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    plan = generate_trip_plan(
        destination=payload.destination,
        budget=payload.budget,
        duration_days=payload.duration_days,
        preferences=payload.preferences or "",
    )

    trip = models.Trip(
        user_id=current_user.user_id,
        destination=payload.destination,
        budget=payload.budget,
        duration_days=payload.duration_days,
        status="planned",
        ai_generated_plan=plan.get("summary", ""),
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    for day in plan.get("days", []):
        db.add(models.ItineraryDay(
            trip_id=trip.trip_id,
            day_number=day.get("day_number", 0),
            activities=day.get("activities", ""),
            estimated_cost=day.get("estimated_cost", 0),
        ))
    db.commit()

    db.add(models.TransactionLog(
        user_id=current_user.user_id,
        action="trip_created",
        details=f"{payload.destination} ({payload.duration_days} days)",
    ))
    db.commit()
    db.refresh(trip)

    # send emai of AI itinerary..otherwise leave it 
    email_service.send_itinerary_email(
        current_user.email, current_user.name, payload.destination, plan
    )
    return trip


@router.get("", response_model=List[schemas.TripOut])
def my_trips(db: Session = Depends(get_db),
             current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Trip)
        .filter(models.Trip.user_id == current_user.user_id)
        .order_by(models.Trip.created_at.desc())
        .all()
    )


@router.get("/{trip_id}", response_model=schemas.TripOut)
def get_trip(trip_id: int, db: Session = Depends(get_db),
             current_user: models.User = Depends(get_current_user)):
    trip = (
        db.query(models.Trip)
        .filter(models.Trip.trip_id == trip_id,
                models.Trip.user_id == current_user.user_id)
        .first()
    )
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=204)
def delete_trip(trip_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    trip = (
        db.query(models.Trip)
        .filter(models.Trip.trip_id == trip_id,
                models.Trip.user_id == current_user.user_id)
        .first()
    )
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
