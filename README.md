# JSM Django - Full Stack Student Management System

A comprehensive school/college management system with Django REST API and React frontend.

## Project Structure

```
jsm_django/
├── backend/                 # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── admin.py
├── frontend/                # React Dashboard
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── context/
│       ├── styles/
│       ├── App.js
│       └── index.js
└── docker-compose.yml
```

## Features

### Backend (Django REST API)
- User Authentication (JWT)
- Role-based Access Control (Admin, Teacher, Student, Parent)
- Student Management
- Course & Subject Management
- Assignment Tracking
- Attendance System
- Payment Management
- Video Lectures
- Results & Performance
- Announcements & Events
- Gallery Management
- Enquiry Management

### Frontend (React)
- Responsive Dashboard
- Student Portal
- Teacher Dashboard
- Admin Management Panel
- Real-time Notifications
- Charts & Analytics
- File Upload/Download
- Calendar Integration

## Setup Instructions

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Documentation

Base URL: `http://localhost:8000/api/`

### Authentication
- POST `/auth/register/` - User registration
- POST `/auth/login/` - Get JWT tokens
- POST `/auth/token/refresh/` - Refresh token
- GET `/auth/profile/` - Get current user profile

## License
MIT
