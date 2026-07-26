

from dotenv import load_dotenv
load_dotenv()  

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.database import Base, engine
from app import models  
from app.routes import auth, hotels, trips, bookings, reviews, payments, admin, profile

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GO-TRAVEL", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(hotels.router, prefix="/api/hotels", tags=["Hotels"])
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(profile.router, prefix="/api", tags=["Profile"])


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/thank-you", response_class=HTMLResponse)
def thankyou_page(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_page(request: Request):
    return templates.TemplateResponse("forgot.html", {"request": request})
@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok", "app": "GO-TRAVEL"}
