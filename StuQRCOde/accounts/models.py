
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Extended User model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class Student(models.Model):
    """Student profile model"""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    program = models.CharField(max_length=100)  # Renamed from department
    level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)], default=1)  # Renamed from year_of_study
    enrollment_year = models.PositiveIntegerField(null=True, blank=True)  # Replaced enrollment_date
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"


class Lecturer(models.Model):
    """Lecturer profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
