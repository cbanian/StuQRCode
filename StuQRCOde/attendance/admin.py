from django.contrib import admin
from .models import QRCode, AttendanceRecord, AttendanceStatistics

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'valid_from', 'valid_until', 'is_active', 'created_by', 'created_at']
    search_fields = ['course__code', 'course__name', 'created_by__user__first_name', 'created_by__user__last_name']
    list_filter = ['is_active', 'created_at', 'valid_from', 'valid_until']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'time_in', 'status', 'marked_by']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id', 'course__code', 'course__name']
    list_filter = ['status', 'date', 'marked_by', 'course__semester']
    readonly_fields = ['time_in']
    ordering = ['-date', '-time_in']

@admin.register(AttendanceStatistics)
class AttendanceStatisticsAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'total_classes', 'attended_classes', 'percentage', 'last_updated']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id', 'course__code', 'course__name']
    list_filter = ['course__semester', 'last_updated']
    readonly_fields = ['last_updated']
    ordering = ['-percentage']
