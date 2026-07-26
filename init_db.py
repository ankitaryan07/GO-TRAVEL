"""init_db.py - Database + hotels (15 states, city-wise) + admin account."""

import random
from app.database import Base, engine, SessionLocal
from app import models
from app.security import hash_password
from app.locations import STATE_CITIES

HOTEL_PREFIXES = [
    "Grand", "Royal", "Comfort", "Heritage", "Paradise", "Sunrise", "Elite",
    "Crown", "Riverside", "Plaza", "Silver", "Golden", "Blue", "Green",
    "Lake View", "Mountain", "City", "Classic", "Premium", "Luxury",
    "Saffron", "Lotus", "Taj", "Mahal", "Peacock", "Star", "Diamond",
    "Orchid", "Sapphire", "Emerald", "Imperial", "Regal", "Serene",
]

HOTEL_SUFFIXES = [
    "Hotel", "Inn", "Residency", "Suites", "Retreat", "Resort",
    "Lodge", "Palace", "Stay", "Homestay", "Boutique", "Villa",
    "Guest House", "Haveli", "Manor",
]

AMENITIES_POOL = [
    "WiFi, Breakfast, AC",
    "WiFi, Pool, Breakfast",
    "WiFi, Pool, Spa, Breakfast, AC",
    "WiFi, Parking, Restaurant",
    "WiFi, Gym, Pool, Bar",
    "WiFi, Breakfast, Room Service",
    "WiFi, AC, Parking, Restaurant",
    "WiFi, Pool, Spa, Gym, Bar",
    "WiFi, AC, Laundry, Breakfast",
    "WiFi, Rooftop, Restaurant, Bar",
    "WiFi, Pool, Kids Zone, Parking",
    "WiFi, AC, Gym, Room Service",
]

PRICE_TIERS = [800, 1000, 1200, 1500, 1800, 2000, 2500, 3000, 3500,
               4000, 4500, 5000, 6000, 7500, 9000, 12000]


def create_tables():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created in go_travel.db")


def add_hotels():
    db = SessionLocal()
    existing = db.query(models.Hotel).count()
    if existing >= 500:
        print(f"Hotels already seeded ({existing}). Skipping.")
        db.close()
        return
    # Clear old if < 500
    if existing > 0:
        db.query(models.Hotel).delete()
        db.commit()

    count = 0
    for state, cities in STATE_CITIES.items():
        for city in cities:
            used_names = set()
            # 10-12 hotels per city → ~750-900 total
            num = random.randint(10, 12)
            for i in range(num):
                # Unique name
                for _ in range(20):
                    name = f"{random.choice(HOTEL_PREFIXES)} {city} {random.choice(HOTEL_SUFFIXES)}"
                    if name not in used_names:
                        used_names.add(name)
                        break
                price = random.choice(PRICE_TIERS)
                rating = round(random.uniform(3.2, 4.9), 1)
                db.add(models.Hotel(
                    name=name, state=state, city=city,
                    price_per_night=price, rating=rating,
                    amenities=random.choice(AMENITIES_POOL),
                    image_url=f"/static/img/hotel{(count % 8) + 1}.jpg",
                ))
                count += 1
    db.commit()
    print(f"Added {count} hotels across {len(STATE_CITIES)} states.")
    db.close()


def add_admin():
    db = SessionLocal()
    if db.query(models.User).filter(models.User.email == "admin@gotravel.com").first():
        print("Admin already exists.")
        db.close()
        return
    db.add(models.User(
        name="Admin", email="admin@gotravel.com",
        password_hash=hash_password("admin123"),
        phone="0000000000", is_admin=1,
    ))
    db.commit()
    print("Admin created -> admin@gotravel.com / admin123")
    db.close()


if __name__ == "__main__":
    create_tables()
    add_hotels()
    add_admin()
    print("\nDatabase ready!")
    print("Admin login: admin@gotravel.com / admin123")
