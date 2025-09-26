from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import QRCode

class QRCodeForm(forms.ModelForm):
    """Form for QR code creation"""
    class Meta:
        model = QRCode
        fields = ['course', 'valid_from', 'valid_until']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'valid_from': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'valid_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter courses based on user role
        if user and user.role == 'lecturer':
            from courses.models import Course
            self.fields['course'].queryset = Course.objects.filter(lecturer=user.lecturer_profile)
    
    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_until = cleaned_data.get('valid_until')
        
        if valid_from and valid_until:
            if valid_from >= valid_until:
                raise forms.ValidationError('Valid until date must be after valid from date.')
            
            # Ensure QR code is valid for at least 1 day
            if valid_until - valid_from < timedelta(days=1):
                raise forms.ValidationError('QR code must be valid for at least 1 day.')
        
        return cleaned_data


class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records"""
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    course = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter courses based on user role
        if user:
            from courses.models import Course
            if user.role == 'lecturer':
                self.fields['course'].queryset = Course.objects.filter(lecturer=user.lecturer_profile)
            elif user.role == 'student':
                # Show courses the student has attended
                self.fields['course'].queryset = Course.objects.filter(
                    attendance_records__student=user.student_profile
                ).distinct()
            else:
                self.fields['course'].queryset = Course.objects.all()
