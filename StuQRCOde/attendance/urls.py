from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # QR Code management URLs
    path('qr-codes/', views.qr_code_list, name='qr_code_list'),
    path('qr-codes/create/', views.qr_code_create, name='qr_code_create'),
    path('qr-codes/<uuid:pk>/', views.qr_code_detail, name='qr_code_detail'),
    path('qr-codes/<uuid:pk>/delete/', views.qr_code_delete, name='qr_code_delete'),
    path('qr-codes/<uuid:pk>/generate/', views.qr_code_generate, name='qr_code_generate'),
    
    # Attendance tracking URLs
    path('scan/<uuid:qr_id>/', views.scan_qr_code, name='scan_qr'),
    path('attendance-records/', views.attendance_record_list, name='attendance_record_list'),
    path('attendance-records/<int:pk>/', views.attendance_record_detail, name='attendance_record_detail'),
    
    # Dashboard URLs
    path('dashboard/lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    
    # Report URLs
    path('reports/course/<int:course_id>/', views.course_attendance_report, name='course_attendance_report'),
    path('reports/student/<int:student_id>/', views.student_attendance_report, name='student_attendance_report'),
    path('reports/', views.attendance_reports, name='attendance_reports'),
    path('analytics/', views.attendance_analytics, name='attendance_analytics'),
]
