from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import timedelta

from accounts.models import Student, Lecturer
from courses.models import Course

class QRCode(models.Model):
    """QR code model for attendance tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='qr_codes')
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"QR Code for {self.course.code} - {self.valid_from.date()} to {self.valid_until.date()}"
    
    @property
    def is_valid(self):
        """Check if QR code is currently valid"""
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until
    
    @property
    def days_remaining(self):
        """Calculate days remaining for QR code validity"""
        if not self.is_active:
            return 0
        now = timezone.now()
        if now > self.valid_until:
            return 0
        return (self.valid_until - now).days


class AttendanceRecord(models.Model):
    """Attendance record model"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    time_in = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.CharField(max_length=20, choices=[('qr_scan', 'QR Scan'), ('manual', 'Manual')])
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', '-time_in']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code} - {self.date}"
    
    @property
    def time_difference(self):
        """Calculate time difference from class start"""
        class_schedule = self.course.schedules.first()
        if class_schedule:
            class_start = timezone.datetime.combine(self.date, class_schedule.start_time)
            return self.time_in - class_start
        return None


class AttendanceStatistics(models.Model):
    """Aggregated attendance statistics"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_stats')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_stats')
    total_classes = models.IntegerField(default=0)
    attended_classes = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code} - {self.percentage}%"
    
    def calculate_percentage(self):
        """Calculate attendance percentage"""
        if self.total_classes > 0:
            self.percentage = round((self.attended_classes / self.total_classes) * 100, 2)
        else:
            self.percentage = 0.00
        return self.percentage
