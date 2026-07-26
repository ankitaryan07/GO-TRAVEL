
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ---------- AUTH ----------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=3, max_length=120)
    password: str = Field(..., min_length=6, max_length=72)
    phone: Optional[str] = Field(None, max_length=15)


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    phone: Optional[str]
    is_admin: int = 0
    photo_url: Optional[str] = None
    theme: Optional[str] = "light"
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- TRIP ----------
class TripCreate(BaseModel):
    destination: str = Field(..., min_length=2, max_length=120)
    budget: float = Field(..., gt=0)
    duration_days: int = Field(..., gt=0, le=60)
    preferences: Optional[str] = Field(None, max_length=300)


class ItineraryDayOut(BaseModel):
    day_id: int
    day_number: int
    activities: Optional[str]
    estimated_cost: float
    model_config = ConfigDict(from_attributes=True)


class TripOut(BaseModel):
    trip_id: int
    destination: str
    budget: float
    duration_days: int
    status: str
    ai_generated_plan: Optional[str]
    created_at: datetime
    itinerary_days: List[ItineraryDayOut] = []
    model_config = ConfigDict(from_attributes=True)


# ---------- HOTEL ----------
class HotelOut(BaseModel):
    hotel_id: int
    name: str
    state: str
    city: str
    price_per_night: float
    rating: float
    amenities: Optional[str]
    image_url: Optional[str]
    model_config = ConfigDict(from_attributes=True)


# ---------- BOOKING ----------
class BookingCreate(BaseModel):
    hotel_id: int
    trip_id: Optional[int] = None
    check_in: datetime
    check_out: datetime


class BookingOut(BaseModel):
    booking_id: int
    hotel_id: int
    trip_id: Optional[int]
    check_in: datetime
    check_out: datetime
    total_amount: float
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------- REVIEW ----------
class ReviewCreate(BaseModel):
    hotel_id: int
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=500)


class ReviewOut(BaseModel):
    review_id: int
    hotel_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------- PAYMENT ----------
class PaymentCreate(BaseModel):
    booking_id: int


class PaymentOrderOut(BaseModel):
    payment_id: int
    order_id: str
    amount: float
    currency: str = "INR"
    key_id: str
    mock: bool


class PaymentVerify(BaseModel):
    payment_id: int
    order_id: str
    razorpay_payment_id: str = "mock_payment"
    razorpay_signature: str = "mock_signature"
