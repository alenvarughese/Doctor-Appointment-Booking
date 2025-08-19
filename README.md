# Doctor Appointment Booking System

A comprehensive web application for booking doctor appointments with separate dashboards for users, doctors, and administrators.

## Features

### 🔐 User Authentication
- User registration and login with JWT tokens
- Role-based access control (User, Doctor, Admin)
- Secure password handling
- Profile management

### 👨‍⚕️ Doctor Management
- Doctor profiles with specializations
- Availability scheduling
- Experience and consultation fee management
- License number verification

### 📅 Appointment Booking
- Real-time availability checking
- Date and time slot selection
- Symptom and notes documentation
- Appointment status tracking (Pending, Confirmed, Cancelled, Completed)

### 🎯 User Dashboards
- **User Dashboard**: Profile management, appointment history
- **Doctor Dashboard**: Patient appointments, schedule management
- **Admin Dashboard**: System overview, user management

### 🎨 Modern UI/UX
- Responsive design for all devices
- Intuitive navigation
- Beautiful animations and transitions
- Professional medical theme

## Tech Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **JWT Authentication** - Secure token-based auth
- **SQLite** - Database (can be easily changed to PostgreSQL/MySQL)
- **CORS Headers** - Cross-origin resource sharing

### Frontend
- **React 19** - User interface library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Hook Form** - Form management
- **React Hot Toast** - Notifications
- **Lucide React** - Icon library
- **Date-fns** - Date manipulation

## Project Structure

```
group project/
├── backend/                          # Django backend
│   ├── appointment_system/          # Main Django project
│   ├── users/                       # User management app
│   ├── doctors/                     # Doctor management app
│   ├── appointments/                # Appointment booking app
│   ├── requirements.txt             # Python dependencies
│   └── manage.py                    # Django management script
├── frontend/                        # React frontend
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   ├── pages/                  # Page components
│   │   ├── context/                # React context
│   │   └── App.js                  # Main app component
│   └── package.json                # Node dependencies
└── README.md                        # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET/PUT /api/auth/profile/` - Profile management

### Doctors
- `GET /api/doctors/` - List all doctors
- `GET /api/doctors/{id}/` - Get doctor details
- `GET /api/specializations/` - List specializations
- `GET /api/doctors/specialization/{id}/` - Doctors by specialization

### Appointments
- `GET/POST /api/appointments/` - List/create appointments
- `GET/PUT/DELETE /api/appointments/{id}/` - Manage appointment
- `POST /api/appointments/{id}/cancel/` - Cancel appointment
- `GET /api/doctors/{id}/available-slots/` - Check availability

## Usage Guide

### For Patients
1. **Register/Login** - Create an account or sign in
2. **Find Doctors** - Browse available doctors by specialization
3. **Book Appointment** - Select date, time, and provide symptoms
4. **Manage Appointments** - View, cancel, or reschedule appointments

### For Doctors
1. **Login** - Access doctor dashboard
2. **View Schedule** - See upcoming appointments
3. **Manage Appointments** - Confirm, cancel, or mark as completed
4. **Update Availability** - Set working hours and availability

### For Administrators
1. **System Overview** - Monitor system statistics
2. **User Management** - Manage user accounts
3. **Doctor Verification** - Approve doctor registrations
4. **System Health** - Monitor application status

## Database Models

### User Model
- Username, email, password
- User type (user/doctor/admin)
- Personal information (name, phone, address, DOB)
- Profile picture

### Doctor Model
- User reference
- Specialization
- License number
- Experience years
- Consultation fee
- Availability status

### Appointment Model
- Patient and doctor references
- Date and time
- Status tracking
- Symptoms and notes
- Timestamps

## Security Features

- JWT token authentication
- Role-based access control
- Password validation
- CORS protection
- Input validation and sanitization

## Customization

### Adding New Specializations
1. Access Django admin at `/admin`
2. Navigate to Specializations
3. Add new specialization with name and description

### Modifying Appointment Duration
Edit the `available_slots` function in `appointments/views.py` to change the default 30-minute slot duration.

### Changing UI Theme
Modify the CSS variables in `frontend/src/App.css` to customize colors and styling.

## Deployment

### Backend Deployment
- Use production database (PostgreSQL/MySQL)
- Set `DEBUG = False` in settings
- Configure static file serving
- Use production WSGI server (Gunicorn)

### Frontend Deployment
- Build the project: `npm run build`
- Serve static files from a web server
- Configure environment variables for API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue in the repository or contact the development team.

---

**Note**: This is a development version. For production use, ensure proper security measures, database optimization, and error handling are implemented.
