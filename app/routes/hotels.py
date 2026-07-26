

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.locations import STATE_CITIES

router = APIRouter()


@router.get("/locations")
def get_locations():
    return STATE_CITIES


@router.get("", response_model=List[schemas.HotelOut])
def list_hotels(db: Session = Depends(get_db)):
    return db.query(models.Hotel).all()


@router.get("/search", response_model=List[schemas.HotelOut])
def search_hotels(
    state: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Hotel)
    if state:
        q = q.filter(models.Hotel.state.ilike(f"%{state}%"))
    if city:
        q = q.filter(models.Hotel.city.ilike(f"%{city}%"))
    if max_price is not None:
        q = q.filter(models.Hotel.price_per_night <= max_price)
    return q.order_by(models.Hotel.rating.desc()).all()


@router.get("/suggest", response_model=List[schemas.HotelOut])
def suggest_hotels(
    state: Optional[str] = Query(None),
    city: str = Query(...),
    db: Session = Depends(get_db),
):
    """State + City se hotels suggest karo — no budget filter."""
    q = db.query(models.Hotel).filter(models.Hotel.city == city)
    if state:
        q = q.filter(models.Hotel.state == state)
    hotels = q.order_by(models.Hotel.rating.desc()).all()
    if not hotels:
        # City exact match nahi mila to ilike try karo
        q2 = db.query(models.Hotel).filter(models.Hotel.city.ilike(f"%{city}%"))
        if state:
            q2 = q2.filter(models.Hotel.state.ilike(f"%{state}%"))
        hotels = q2.order_by(models.Hotel.rating.desc()).all()
    return hotels


@router.get("/{hotel_id}", response_model=schemas.HotelOut)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel
