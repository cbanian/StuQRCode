from django.contrib import admin
from .models import Semester, Course, ClassSchedule

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'start_date', 'end_date', 'is_active']
    list_filter = ['name', 'year', 'is_active']
    search_fields = ['name', 'year']
    ordering = ['-year', '-start_date']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'lecturer', 'semester', 'credit_hours', 'created_at']
    search_fields = ['code', 'name', 'lecturer__user__first_name', 'lecturer__user__last_name']
    list_filter = ['semester', 'credit_hours', 'created_at']
    ordering = ['code']

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'day', 'start_time', 'end_time', 'room']
    search_fields = ['course__code', 'course__name', 'room']
    list_filter = ['day', 'course__semester']
    ordering = ['course', 'day', 'start_time']
