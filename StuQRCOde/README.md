# Student Registration & Attendance Web Application with QR Code Scanning

A comprehensive Django-based web application for managing student registration and attendance tracking using QR code scanning technology.

## Features

### Admin Panel
- Create and manage courses/modules
- Generate time-bound QR codes for each course
- View attendance statistics and export reports
- User management (students, lecturers, admins)

### Lecturer Dashboard
- View attendance records by class/module
- Analyze attendance statistics over time
- Generate and manage QR codes
- Export attendance reports

### Student Portal
- Secure sign up and login
- Scan QR codes to mark attendance
- View personal attendance history and percentage
- Download attendance reports

### QR Code Attendance Tracking
- Each QR code is valid for a specific period (configurable)
- Automatic date & time recording upon scanning
- Duplicate attendance prevention
- Mobile-friendly scanning interface

### Reports & Analytics
- Attendance summary by student and class
- Exportable reports (PDF/Excel)
- Real-time statistics dashboard
- Custom date range filtering

## Technology Stack

- **Backend**: Django 5.1.4 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **QR Code Generation**: Python qrcode library
- **Report Generation**: ReportLab (PDF), OpenPyXL (Excel)

## Project Structure

```
StuQRCOde/
├── accounts/           # User management (students, lecturers, admins)
├── courses/            # Course and class schedule management
├── attendance/         # QR codes and attendance tracking
├── dashboard/          # Analytics and reporting
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, images
└── StuQRCOde/          # Django project settings
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.1.4
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StuQRCOde
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Admin Panel: http://localhost:8000/admin/
   - Main Application: http://localhost:8000/

## Usage Guide

### For Administrators
1. Log in to the admin panel
2. Create semesters, courses, and assign lecturers
3. Generate QR codes for each course
4. Monitor system-wide attendance statistics

### For Lecturers
1. Register as a lecturer and complete profile
2. Create courses and class schedules
3. Generate QR codes for attendance
4. View and analyze attendance reports

### For Students
1. Register as a student and complete profile
2. Scan QR codes displayed in classrooms
3. View personal attendance history
4. Download attendance certificates

## QR Code Usage

1. **Generate QR Code**: Lecturer creates a QR code valid for a specific period
2. **Display QR Code**: Print and display the QR code in the classroom
3. **Scan QR Code**: Students scan using their mobile devices
4. **Mark Attendance**: System automatically records attendance with timestamp

## API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/profile/` - User profile

### Courses
- `GET /courses/` - List all courses
- `POST /courses/create/` - Create new course
- `GET /courses/<id>/` - Course details

### Attendance
- `GET /attendance/qr-codes/` - List QR codes
- `POST /attendance/qr-codes/create/` - Create QR code
- `GET /attendance/scan/<qr_id>/` - Scan QR code for attendance
- `GET /attendance/dashboard/student/` - Student dashboard
- `GET /attendance/dashboard/lecturer/` - Lecturer dashboard

## Database Models

### User Management
- **User**: Extended Django user model with role-based access
- **Student**: Student profile with student ID and department
- **Lecturer**: Lecturer profile with employee ID and department

### Course Management
- **Semester**: Academic semester management
- **Course**: Course/module information
- **ClassSchedule**: Weekly class schedules

### Attendance Tracking
- **QRCode**: Time-bound QR codes for attendance
- **AttendanceRecord**: Individual attendance entries
- **AttendanceStatistics**: Aggregated attendance data

## Development

### Adding New Features
1. Create appropriate models in respective apps
2. Add views and forms
3. Create templates
4. Update URLs
5. Run migrations

### Testing
```bash
python manage.py test
```

### Production Deployment
1. Update settings for production
2. Configure PostgreSQL database
3. Set up static files serving
4. Configure web server (Nginx/Apache)
5. Set up SSL certificates

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support and questions, please contact the development team or create an issue in the repository.
