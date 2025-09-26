from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course management URLs
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Class schedule URLs
    path('<int:course_id>/schedule/add/', views.schedule_add, name='schedule_add'),
    path('schedule/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedule/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
    
    # Course assignments management
    path('assignments/', views.course_assignments, name='course_assignments'),
    
    # My courses view for students
    path('my-courses/', views.my_courses, name='my_courses'),
]
