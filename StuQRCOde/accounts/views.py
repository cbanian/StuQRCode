from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .forms import UserRegistrationForm, StudentProfileForm, LecturerProfileForm, UserLoginForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .models import User, Student, Lecturer

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please complete your profile.')
            
            # Redirect to profile completion based on role
            if user.role == 'student':
                return redirect('accounts:complete_student_profile')
            elif user.role == 'lecturer':
                return redirect('accounts:complete_lecturer_profile')
            else:
                login(request, user)
                return redirect('dashboard:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect('admin:index')
                elif user.role == 'lecturer':
                    return redirect('dashboard:lecturer_dashboard')
                else:  # student
                    # Check if student profile is complete
                    try:
                        student = user.student_profile
                        if not student.date_of_birth:  # Proxy for completion; add more checks if needed
                            messages.info(request, 'Please complete your student profile.')
                            return redirect('accounts:complete_student_profile')
                    except Student.DoesNotExist:
                        messages.info(request, 'Please complete your student profile.')
                        return redirect('accounts:complete_student_profile')
                    return redirect('dashboard:student_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def complete_student_profile(request):
    """Complete student profile after registration or login if incomplete"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    student = None
    is_complete = False
    try:
        student = request.user.student_profile
        if student.date_of_birth:  # Proxy for completion
            is_complete = True
            messages.info(request, 'Profile already completed.')
            return redirect('dashboard:student_dashboard')
    except Student.DoesNotExist:
        pass
    
    if request.method == 'POST':
        if student:
            form = StudentProfileForm(request.POST, instance=student)
        else:
            form = StudentProfileForm(request.POST)
        if form.is_valid():
            student = form.save(user=request.user)
            messages.success(request, 'Student profile completed successfully!')
            return redirect('dashboard:student_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if student:
            form = StudentProfileForm(instance=student)
        else:
            form = StudentProfileForm()
    
    return render(request, 'accounts/complete_student_profile.html', {'form': form})


@login_required
def complete_lecturer_profile(request):
    """Complete lecturer profile after registration"""
    if request.user.role != 'lecturer':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    try:
        lecturer = request.user.lecturer_profile
        messages.info(request, 'Profile already completed.')
        return redirect('dashboard:lecturer_dashboard')
    except Lecturer.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST)
        if form.is_valid():
            lecturer = form.save(commit=False)
            lecturer.user = request.user
            lecturer.save()
            messages.success(request, 'Lecturer profile completed successfully!')
            return redirect('dashboard:lecturer_dashboard')
    else:
        form = LecturerProfileForm()
    
    return render(request, 'accounts/complete_lecturer_profile.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    
    context = {
        'user': user,
    }
    
    if user.role == 'student':
        try:
            context['student'] = user.student_profile
        except Student.DoesNotExist:
            pass
    elif user.role == 'lecturer':
        try:
            context['lecturer'] = user.lecturer_profile
        except Lecturer.DoesNotExist:
            pass
    
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile"""
    user = request.user
    
    if request.method == 'POST':
        if user.role == 'student':
            try:
                student = user.student_profile
                form = StudentProfileForm(request.POST, instance=student)
            except Student.DoesNotExist:
                form = StudentProfileForm(request.POST)
            
            if form.is_valid():
                student = form.save(user=user)
                messages.success(request, 'Student profile updated successfully!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Please correct the errors below.')
                
        elif user.role == 'lecturer':
            try:
                lecturer = user.lecturer_profile
                form = LecturerProfileForm(request.POST, instance=lecturer)
            except Lecturer.DoesNotExist:
                form = LecturerProfileForm(request.POST)
            
            if form.is_valid():
                lecturer = form.save(commit=False)
                lecturer.user = user
                lecturer.save()
                messages.success(request, 'Lecturer profile updated successfully!')
                return redirect('accounts:profile')
        else:
            messages.error(request, 'Invalid role for profile editing.')
            return redirect('accounts:profile')
    else:
        if user.role == 'student':
            try:
                student = user.student_profile
                student_form = StudentProfileForm(instance=student)
            except Student.DoesNotExist:
                student_form = StudentProfileForm()
            context = {'student_form': student_form, 'lecturer_form': None}
            
        elif user.role == 'lecturer':
            try:
                lecturer = user.lecturer_profile
                lecturer_form = LecturerProfileForm(instance=lecturer)
            except Lecturer.DoesNotExist:
                lecturer_form = LecturerProfileForm()
            context = {'lecturer_form': lecturer_form, 'student_form': None}
        else:
            context = {'student_form': None, 'lecturer_form': None}
    
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


def password_reset_request_view(request):
    """View for requesting password reset"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # Create reset link
                reset_url = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                # Send email
                subject = 'Password Reset Request'
                message = f'Hi {user.get_full_name()},\n\nYou requested a password reset. Click the link below to reset your password:\n\n{reset_url}\n\nIf you did not request this, please ignore this email.'
                html_message = f'Hi {user.get_full_name()},<br><br>You requested a password reset. Click the link below to reset your password:<br><br><a href="{reset_url}">Reset Password</a><br><br>If you did not request this, please ignore this email.'
                send_mail(subject, message, 'noreply@stuattend.com', [email], html_message=html_message)
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    """View for confirming password reset"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('accounts:login')
        else:
            form = PasswordResetConfirmForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('accounts:password_reset_request')
