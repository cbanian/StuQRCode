from django import forms
from .models import Course, ClassSchedule

class CourseForm(forms.ModelForm):
    """Form for course creation and editing"""
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credit_hours', 'lecturer', 'semester']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'credit_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'lecturer': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }


class ClassScheduleForm(forms.ModelForm):
    """Form for class schedule creation and editing"""
    
    class Meta:
        model = ClassSchedule
        fields = ['day', 'start_time', 'end_time', 'room']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
        }
