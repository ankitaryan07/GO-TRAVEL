<h1 align="center">GO-TRAVEL</h1>
<p align="center">
  <b>An AI-powered travel booking platform built for MCA final year project'26</b><br/>
  Intelligent travel recommendations, seamless booking experience, and personalized itinerary planning powered by cutting-edge AI.
</p>
<p align="center">
Project Name : GO-TRAVEL - AI-Powered Travel Booking Platform<br/>
Guided By : Prof. Dr. Amit Kumar Shukla Sir<br/>
Learner Name : Ankit Aryan <br/>
College : 711- CIMAGE Center of Digital Technology and Entrepreneurship, Patna<br/>
Course : Master of Computer Applications<br/>
University : ARYABHATTA KNOWLEDGE UNIVERSITY, PATNA<br/>
ENROLLMENT : 24326711015<br/>
Session : 2024-2026<br/>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/MCA-Final%20Year%20Project-blueviolet" />
  <img src="https://img.shields.io/badge/Built%20With-FastAPI%20%7C%20SQLite%20%7C%20CrewAI%20%7C%20Razorpay-informational" />
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" />
</p>

---

## 🔍 Overview

GO-TRAVEL is a full-stack, AI-driven platform that revolutionizes travel planning and booking. Using advanced multi-agent AI systems, it provides intelligent destination recommendations, curated itineraries, and seamless payment integration. Designed to aid travelers in discovering perfect travel experiences with real-time insights, personalized suggestions, and a beautiful, intuitive user interface.

> 🏆 Built for MCA Final Year Project - Aryabhatta Knowledge University, Patna

---

## ✨ Key Features

- **🤖 AI-Powered Recommendations**  
  Multi-agent CrewAI system with Researcher & Planner agents for intelligent suggestions

- **🎯 Smart Destination Search**  
  Advanced location-based search with filters and personalized preferences

- **✈️ Flight & Hotel Integration**  
  Real-time availability and booking for flights and accommodations

- **💳 Secure Payment Processing**  
  Razorpay integration for safe and reliable transactions

- **📧 Email Notifications**  
  SendGrid integration for booking confirmations and updates

- **🔐 Robust Authentication**  
  OTP-based verification and JWT token management

- **👥 User Dashboard**  
  Track bookings, manage profiles, and view travel history

- **👨‍💼 Admin Panel**  
  Comprehensive dashboard for system management and analytics

- **📊 Real-Time Analytics**  
  Track bookings, revenue, user engagement, and system performance

---

## 🛠️ Tech Stack

| Frontend              | Backend/Database         | AI & Integration        |
|----------------------|--------------------------|------------------------|
| HTML5, CSS3          | FastAPI                  | CrewAI                  |
| JavaScript (Vanilla) | SQLite (11 Tables)       | Llama 3 (Ollama)        |
| Responsive Design    | SQLAlchemy ORM           | Razorpay API            |
|                      | Python 3.8+              | SendGrid + Gmail SMTP   |
|                      | Uvicorn Server           | OTP Authentication      |

---

## 📁 Project Structure

```
GO-TRAVEL/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # SQLite configuration & session management
│   ├── models.py               # SQLAlchemy ORM models (11 database tables)
│   ├── schemas.py              # Pydantic request/response validation schemas
│   ├── routes/                 # API endpoint handlers
│   ├── ai_service.py           # CrewAI + Llama 3 integration
│   ├── email_service.py        # SendGrid + Gmail SMTP integration
│   ├── payment_service.py      # Razorpay payment gateway integration
│   ├── security.py             # OTP generation & JWT authentication logic
│   ├── dependencies.py         # FastAPI dependency injection utilities
│   ├── validators.py           # Data validation functions
│   └── locations.py            # Location database & utilities
│
├── templates/                  # Frontend HTML Templates
│   ├── index.html             # Homepage with hero section
│   ├── login.html             # User login page
│   ├── signup.html            # User registration page
│   ├── dashboard.html         # User booking dashboard
│   ├── profile.html           # User profile management
│   ├── admin.html             # Admin control panel
│   ├── forgot.html            # Password recovery page
│   └── thankyou.html          # Booking confirmation page
│
├── static/                     # Static Assets
│   ├── css/                   # Stylesheets (main.css, responsive.css)
│   ├── js/                    # JavaScript (main.js, api.js, utils.js)
│   └── img/                   # Images & icons
│
├── go_travel.db               # SQLite Database with 11 normalized tables
├── init_db.py                 # Database schema initialization script
├── requirements.txt           # Python package dependencies
├── .env.example              # Example environment configuration
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## 📊 Database Schema

GO-TRAVEL uses SQLite with **11 normalized tables**:

1. **users** - User accounts, authentication, and profiles
2. **bookings** - Travel booking records and status
3. **hotels** - Hotel listings and availability
4. **flights** - Flight information and schedules
5. **locations** - Travel destinations and descriptions
6. **reviews** - User reviews and ratings
7. **payments** - Transaction records and status
8. **itineraries** - Custom travel plans
9. **preferences** - User travel preferences
10. **admin_logs** - Administrative activity logs
11. **feedback** - User feedback and suggestions

---

## 🖼️ Demo Preview

### 🏠 Landing Page - Hero Section
<p align="center">
  <img width="1600" height="800" alt="landing" src="https://via.placeholder.com/1600x800?text=GO-TRAVEL+Landing+Page" />
</p><br/>

---

### ✍️ User Registration
<p align="center">
  <img width="1600" height="800" alt="signup" src="https://via.placeholder.com/1600x800?text=GO-TRAVEL+Sign+Up+Page" />
</p><br/>

---

### 🔐 User Login
<p align="center">
  <img width="1600" height="800" alt="signin" src="https://via.placeholder.com/1600x800?text=GO-TRAVEL+Sign+In+Page" />
</p><br/>

---

### 🔍 Search & Explore
<p align="center">
  <img width="1600" height="800" alt="search" src="https://via.placeholder.com/1600x800?text=GO-TRAVEL+Search+Destinations" />
</p><br/>

---

### 🤖 AI Recommendations
<p align="center">
  <img width="1600" height="800" alt="recommendations" src="https://via.placeholder.com/1600x800?text=AI+Powered+Recommendations" />
</p><br/>

---

### 📊 User Dashboard
<p align="center">
  <img width="1600" height="800" alt="dashboard" src="https://via.placeholder.com/1600x800?text=GO-TRAVEL+User+Dashboard" />
</p><br/>

---

### 💳 Payment & Checkout
<p align="center">
  <img width="1600" height="800" alt="payment" src="https://via.placeholder.com/1600x800?text=Secure+Payment+Checkout" />
</p><br/>

---

### 👨‍💼 Admin Panel
<p align="center">
  <img width="1600" height="800" alt="admin" src="https://via.placeholder.com/1600x800?text=Admin+Control+Panel" />
</p><br/>

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Ollama (for local LLM deployment)
- Modern web browser

### Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/MCA-711-1246-Ankitaryan/GO-TRAVEL.git
cd GO-TRAVEL
```

**2. Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**
```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your API keys:
# RAZORPAY_KEY_ID=your_razorpay_key
# RAZORPAY_KEY_SECRET=your_razorpay_secret
# SENDGRID_API_KEY=your_sendgrid_key
# GMAIL_EMAIL=your_email@gmail.com
# GMAIL_PASSWORD=your_app_password
# OLLAMA_API_URL=http://localhost:11434
```

**5. Initialize database:**
```bash
python init_db.py
```

**6. Start the application:**
```bash
uvicorn app.main:app --reload
```

**7. Access the application:**
```
Frontend: http://localhost:8000
API Documentation: http://localhost:8000/docs
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/send-otp` - Send OTP verification
- `POST /api/auth/verify-otp` - Verify OTP
- `POST /api/auth/logout` - User logout

### Destinations & Search
- `GET /api/locations` - List all travel destinations
- `GET /api/locations/{id}` - Get destination details
- `GET /api/search` - Search flights and hotels
- `GET /api/recommendations` - Get AI-powered recommendations

### Bookings
- `GET /api/bookings` - List user bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}` - Update booking
- `DELETE /api/bookings/{id}` - Cancel booking

### Payments
- `POST /api/payments/create-order` - Create Razorpay order
- `POST /api/payments/verify` - Verify payment
- `GET /api/payments/{id}` - Get payment status

### User Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile
- `GET /api/favorites` - Get favorite locations

### Admin
- `GET /api/admin/users` - List all users
- `GET /api/admin/bookings` - All bookings
- `GET /api/admin/analytics` - Dashboard analytics
- `GET /api/admin/payments` - Payment records

See full API documentation at `/docs` endpoint.

---

## 🤖 AI Features

### CrewAI Multi-Agent System

GO-TRAVEL uses CrewAI with Llama 3 (via Ollama) for intelligent travel planning:

**Researcher Agent**
- Analyzes user preferences and travel history
- Researches destinations based on criteria
- Finds best flight and hotel options
- Identifies attractions and activities

**Planner Agent**
- Creates personalized itineraries
- Optimizes travel routes and schedules
- Suggests activities and experiences
- Provides budget recommendations

### Integration Points
- Real-time destination analysis
- Smart recommendation engine
- Personalized itinerary generation
- Travel expense optimization

---

## 💳 Payment Integration

### Razorpay Integration
- Secure payment processing
- Multiple payment methods support
- Automatic order confirmation
- Refund management
- Transaction tracking

### Payment Flow
1. User selects booking
2. System creates Razorpay order
3. User completes payment
4. Payment verification
5. Booking confirmation

---

## 📧 Communication Services

### SendGrid Email Integration
- Professional email templates
- Booking confirmations
- Itinerary details
- Promotional emails
- Support communications

### Gmail SMTP Backup
- Fallback email service
- User notifications
- Password reset emails
- System alerts

---

## 🔐 Security Features

- **OTP Authentication** - Two-factor verification for user accounts
- **JWT Tokens** - Secure session management
- **Password Hashing** - bcrypt for password security
- **CORS Protection** - Cross-origin request handling
- **Input Validation** - Pydantic schema validation
- **SQL Injection Prevention** - SQLAlchemy parameterized queries
- **Environment Secrets** - API keys in .env file

---

## 📊 Features Breakdown

### User Features
✅ Registration & Login with OTP  
✅ Search destinations worldwide  
✅ AI-powered travel recommendations  
✅ Book flights and hotels  
✅ Create custom itineraries  
✅ View booking history  
✅ Download trip details  
✅ Rate and review experiences  
✅ Save favorite destinations  
✅ Manage payment methods  

### Admin Features
✅ User management  
✅ Booking oversight  
✅ Payment tracking  
✅ System analytics  
✅ Destination management  
✅ Promotional management  
✅ Report generation  
✅ Activity logging  

---

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack web application development
- RESTful API design and implementation
- Database design with normalization
- AI/ML integration with LLMs
- Third-party API integration
- User authentication and authorization
- Responsive web design principles
- Professional project structure
- Version control with Git

---

## 🛡️ Best Practices Used

- Clean code architecture
- Separation of concerns
- DRY principle (Don't Repeat Yourself)
- SOLID design principles
- Comprehensive error handling
- Input validation and sanitization
- API documentation
- Code comments and docstrings
- Environment-based configuration
- Security best practices

---

## 📝 Environment Configuration

Create `.env` file with following variables:

```env
# Database
DATABASE_URL=sqlite:///./go_travel.db

# API Keys
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
SENDGRID_API_KEY=your_key

# Email
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# AI/LLM
OLLAMA_API_URL=http://localhost:11434

# JWT
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Application
APP_NAME=GO-TRAVEL
APP_VERSION=1.0.0
DEBUG=True
```

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact via email
- Check documentation at `/docs`

---

## 🙏 Acknowledgments

- CIMAGE Center of Digital Technology and Entrepreneurship, Patna
- Aryabhatta Knowledge University
- Faculty Guide: [Prof. Name]
- FastAPI & Python communities
- CrewAI framework developers
- Razorpay & SendGrid for APIs

---

## 📜 License

This project is for educational purposes as part of MCA Final Year Project requirements.

---

## 👨‍💻 Project Details

| Aspect | Details |
|--------|---------|
| **Project Name** | GO-TRAVEL |
| **Type** | Full-Stack Web Application |
| **Duration** | 6 Months (Jan 2025 - July 2026) |
| **Student** | Ankit Aryan  |
| **Enrollment** | 24326711015 |
| **Session** | 2024-2026 |
| **College** | CIMAGE, Patna |
| **University** | Aryabhatta Knowledge University |
| **Course** | MCA (Master of Computer Applications) |
| **Status** | ✅ Completed |

---

<p align="center">
  <strong>Made with ❤️ by Ankit Aryan</strong><br/>
  <strong>MCA Final Year Project - Aryabhatta Knowledge University, Patna</strong><br/>
  <strong>© 2026 - All Rights Reserved</strong>
</p>

---

Last Updated: July 24, 2026  
**Status:** ✅ Complete & Production Ready
