from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
]
