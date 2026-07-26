"""GO-TRAVEL database models — 8 tables."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    is_admin = Column(Integer, default=0)  
    photo_url = Column(Text, nullable=True)       # profile photo (base64 or url)
    theme = Column(String(10), default="light")   # light / dark
    created_at = Column(DateTime, default=datetime.utcnow)

    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("TransactionLog", back_populates="user", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="user", cascade="all, delete-orphan")


class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    destination = Column(String(120), nullable=False)
    budget = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    status = Column(String(30), default="planned")
    ai_generated_plan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="trips")
    itinerary_days = relationship("ItineraryDay", back_populates="trip", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="trip")


class Hotel(Base):
    __tablename__ = "hotels"
    hotel_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    state = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    price_per_night = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    amenities = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)

    bookings = relationship("Booking", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=True)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    hotel = relationship("Hotel", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), default="razorpay")
    txn_id = Column(String(120), nullable=True)
    status = Column(String(30), default="created")
    paid_at = Column(DateTime, nullable=True)

    booking = relationship("Booking", back_populates="payment")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"
    day_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    activities = Column(Text, nullable=True)
    estimated_cost = Column(Float, default=0.0)

    trip = relationship("Trip", back_populates="itinerary_days")


class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")


class TransactionLog(Base):
    __tablename__ = "transactions_log"
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")


class OTPCode(Base):
    """Forgot-password OTP verification ke liye."""
    __tablename__ = "otp_codes"
    otp_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PaymentMethod(Base):
    """User ke saved cards / UPI (project demo ke liye — last 4 digits store)."""
    __tablename__ = "payment_methods"
    method_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    method_type = Column(String(20), nullable=False)   # "card" or "upi"
    label = Column(String(100), nullable=True)         # "HDFC Debit", "GPay"
    masked_value = Column(String(50), nullable=True)   # "**** **** **** 1234" or "user@upi"
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payment_methods")
