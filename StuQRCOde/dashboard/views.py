from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import Student, Lecturer
from attendance.models import QRCode, AttendanceRecord
from courses.models import Course, ClassSchedule

def home(request):
    """Home dashboard view"""
    return render(request, 'dashboard/home.html')

@login_required
def lecturer_dashboard(request):
    """Lecturer dashboard view"""
    if request.user.role != 'lecturer':
        messages.error(request, 'Access denied. You do not have permission to access this page.')
        return redirect('dashboard:home')

    try:
        lecturer = request.user.lecturer_profile
    except Lecturer.DoesNotExist:
        messages.error(request, 'Lecturer profile not found.')
        return redirect('accounts:complete_lecturer_profile')

    # Get courses taught by this lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    # Calculate statistics
    qr_codes_count = QRCode.objects.filter(course__lecturer=lecturer).count()
    students_count = Student.objects.filter(attendance_records__course__lecturer=lecturer).distinct().count()
    courses_count = courses.count()
    attendance_today = AttendanceRecord.objects.filter(
        course__lecturer=lecturer,
        date=timezone.now().date()
    ).count()

    # Recent attendance
    recent_attendance = AttendanceRecord.objects.filter(
        course__lecturer=lecturer
    ).select_related('student', 'course').order_by('-date', '-time_in')[:5]

    # Today's sessions
    today_day = timezone.now().strftime('%A')
    todays_sessions = ClassSchedule.objects.filter(
        course__lecturer=lecturer,
        day=today_day
    ).select_related('course').order_by('start_time')

    context = {
        'qr_codes_count': qr_codes_count,
        'students_count': students_count,
        'courses_count': courses_count,
        'attendance_today': attendance_today,
        'recent_attendance': recent_attendance,
        'todays_sessions': todays_sessions,
    }

    return render(request, 'dashboard/lecturer_dashboard.html', context)

@login_required
def student_dashboard(request):
    """Student dashboard view"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied. You do not have permission to access this page.')
        return redirect('dashboard:home')
    
    # Check if student profile is complete
    try:
        student = request.user.student_profile
        if not student.date_of_birth:  # Proxy for completion
            messages.info(request, 'Please complete your student profile.')
            return redirect('accounts:complete_student_profile')
    except Student.DoesNotExist:
        messages.info(request, 'Please complete your student profile.')
        return redirect('accounts:complete_student_profile')
    
    return render(request, 'dashboard/student_dashboard.html')
