from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Lecturer

class CustomUserAdmin(UserAdmin):
    """Custom User Admin with role-based fields"""
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone'),
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'program', 'level', 'enrollment_year']
    search_fields = ['user__first_name', 'user__last_name', 'student_id', 'program']
    list_filter = ['program', 'level', 'enrollment_year']
    readonly_fields = []

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'qualification', 'hire_date']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id', 'department']
    list_filter = ['department', 'hire_date']
    readonly_fields = ['hire_date']

admin.site.register(User, CustomUserAdmin)
