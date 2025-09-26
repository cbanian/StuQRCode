from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, ClassSchedule
from .forms import CourseForm, ClassScheduleForm
from accounts.models import User, Student

@login_required
def course_list(request):
    """List all courses"""
    courses = Course.objects.all().select_related('lecturer', 'semester')

    # Filter by role
    if request.user.role == 'lecturer':
        try:
            lecturer_profile = request.user.lecturer_profile
            courses = courses.filter(lecturer=lecturer_profile)
        except User.lecturer_profile.RelatedObjectDoesNotExist:
            messages.warning(request, 'You do not have a lecturer profile. Please contact administrator.')
            courses = Course.objects.none()
    elif request.user.role == 'student':
        # Check if student profile is complete
        try:
            student_profile = request.user.student_profile
            if not student_profile.date_of_birth:  # Proxy for completion
                messages.info(request, 'Please complete your student profile.')
                return redirect('accounts:complete_student_profile')
            # For now, show all courses - implement enrollment filtering later
            pass
        except Student.DoesNotExist:
            messages.info(request, 'Please complete your student profile.')
            return redirect('accounts:complete_student_profile')

    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_list.html', context)


@login_required
def course_detail(request, pk):
    """Course detail view"""
    course = get_object_or_404(Course, pk=pk)

    # Check permissions
    if request.user.role == 'student':
        # Check if student profile is complete
        try:
            student_profile = request.user.student_profile
            if not student_profile.date_of_birth:  # Proxy for completion
                messages.info(request, 'Please complete your student profile.')
                return redirect('accounts:complete_student_profile')
        except Student.DoesNotExist:
            messages.info(request, 'Please complete your student profile.')
            return redirect('accounts:complete_student_profile')
    elif request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile:
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')

    schedules = course.schedules.all()

    context = {
        'course': course,
        'schedules': schedules,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def course_create(request):
    """Create new course"""
    if request.user.role not in ['admin', 'lecturer']:
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            # Send email notifications to all students
            try:
                students = Student.objects.all()
                subject = f'New Course Added: {course.code} - {course.name}'
                message = f'Dear Student,\n\nA new course has been added to the system:\n\nCourse: {course.name}\nCode: {course.code}\nDescription: {course.description}\nCredits: {course.credit_hours}\nLecturer: {course.lecturer.user.get_full_name()}\nSemester: {course.semester}\n\nPlease check the course list for more details.\n\nBest regards,\nStuAttend Team'
                for student in students:
                    if student.user.email:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [student.user.email],
                            fail_silently=True,
                        )
            except Exception:
                # Log error if needed, but don't fail the course creation
                pass
            messages.success(request, 'Course created successfully! Notifications sent to students.')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_edit(request, pk):
    """Edit course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.user.role not in ['admin', 'lecturer'] or (request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile):
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_delete(request, pk):
    """Delete course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.user.role not in ['admin', 'lecturer'] or (request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile):
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses:course_list')
    
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


# Schedule management views
@login_required
def schedule_add(request, course_id):
    """Add class schedule to course"""
    course = get_object_or_404(Course, pk=course_id)
    
    if request.user.role not in ['admin', 'lecturer'] or (request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile):
        messages.error(request, 'Access denied.')
        return redirect('courses:course_detail', pk=course_id)
    
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.course = course
            schedule.save()
            # Send email notifications to all students
            try:
                students = Student.objects.all()
                subject = f'New Schedule Added for {course.code} - {course.name}'
                message = f'Dear Student,\n\nA new class schedule has been added for the course:\n\nCourse: {course.name}\nCode: {course.code}\n\nSchedule Details:\nDay: {schedule.day}\nTime: {schedule.start_time} - {schedule.end_time}\nRoom: {schedule.room}\n\nPlease make note of this schedule.\n\nBest regards,\nStuAttend Team'
                for student in students:
                    if student.user.email:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [student.user.email],
                            fail_silently=True,
                        )
            except Exception:
                # Log error if needed, but don't fail the schedule addition
                pass
            messages.success(request, 'Schedule added successfully! Notifications sent to students.')
            return redirect('courses:course_detail', pk=course_id)
    else:
        form = ClassScheduleForm()
    
    return render(request, 'courses/schedule_form.html', {'form': form, 'course': course})


@login_required
def schedule_edit(request, pk):
    """Edit class schedule"""
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    course = schedule.course
    
    if request.user.role not in ['admin', 'lecturer'] or (request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile):
        messages.error(request, 'Access denied.')
        return redirect('courses:course_detail', pk=course.pk)
    
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully!')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = ClassScheduleForm(instance=schedule)
    
    return render(request, 'courses/schedule_form.html', {'form': form, 'course': course})


@login_required
def schedule_delete(request, pk):
    """Delete class schedule"""
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    course = schedule.course
    
    if request.user.role not in ['admin', 'lecturer'] or (request.user.role == 'lecturer' and course.lecturer != request.user.lecturer_profile):
        messages.error(request, 'Access denied.')
        return redirect('courses:course_detail', pk=course.pk)
    
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully!')
        return redirect('courses:course_detail', pk=course.pk)
    
    return render(request, 'courses/schedule_confirm_delete.html', {'schedule': schedule, 'course': course})


@login_required
def course_assignments(request):
    """Manage course assignments (for lecturers)"""
    if request.user.role not in ['admin', 'lecturer']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    # Get courses based on user role
    if request.user.role == 'lecturer':
        try:
            lecturer_profile = request.user.lecturer_profile
            courses = Course.objects.filter(lecturer=lecturer_profile)
        except User.lecturer_profile.RelatedObjectDoesNotExist:
            messages.warning(request, 'You do not have a lecturer profile. Please complete your profile first.')
            return redirect('accounts:complete_lecturer_profile')
    else:
        courses = Course.objects.all()
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_assignments.html', context)


@login_required
def my_courses(request):
    """Display courses for the logged-in student"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied. This page is for students only.')
        return redirect('dashboard:home')
    
    # Check if student profile is complete
    try:
        student_profile = request.user.student_profile
        if not student_profile.date_of_birth:  # Proxy for completion
            messages.info(request, 'Please complete your student profile.')
            return redirect('accounts:complete_student_profile')
        # For now, show all courses - implement enrollment filtering later
        courses = Course.objects.all().select_related('lecturer', 'semester')
    except Student.DoesNotExist:
        messages.info(request, 'Please complete your student profile.')
        return redirect('accounts:complete_student_profile')
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/my_courses.html', context)
