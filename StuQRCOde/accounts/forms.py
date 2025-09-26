from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, Student, Lecturer

class UserRegistrationForm(UserCreationForm):
    """Form for user registration with role selection"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial='student')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    """Form for student profile completion"""
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Optional phone number"
    )
    
    class Meta:
        model = Student
        fields = ['student_id', 'program', 'level', 'enrollment_year', 'date_of_birth', 'gender', 'address']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '2000', 'max': '2030'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def save(self, commit=True, user=None):
        student = super().save(commit=False)
        if user:
            student.user = user
        if commit:
            student.save()
            if self.cleaned_data['phone']:
                user.phone = self.cleaned_data['phone']
                user.save()
        return student


class LecturerProfileForm(forms.ModelForm):
    """Form for lecturer profile completion"""
    class Meta:
        model = Lecturer
        fields = ['employee_id', 'department', 'qualification']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(forms.Form):
    """Form for user login"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PasswordResetRequestForm(forms.Form):
    """Form for requesting password reset"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Enter your registered email address"
    )


class PasswordResetConfirmForm(SetPasswordForm):
    """Form for confirming password reset"""
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
