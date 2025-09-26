from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Lecturer

class Semester(models.Model):
    """Semester model for organizing courses"""
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    
    name = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    year = models.IntegerField(
        validators=[MinValueValidator(2020), MaxValueValidator(2030)]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['name', 'year']
        ordering = ['-year', '-start_date']
    
    def __str__(self):
        return f"{self.name} {self.year}"


class Course(models.Model):
    """Course/Module model"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    credit_hours = models.IntegerField(default=3)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='courses')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ClassSchedule(models.Model):
    """Class schedule for courses"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ['course', 'day', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}-{self.end_time}"
