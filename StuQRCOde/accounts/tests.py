from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Student, Lecturer

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'student')
        self.assertEqual(str(user), 'Test User (student)')

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password='password123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='student@example.com',
            username='student',
            first_name='Student',
            last_name='User',
            password='password123'
        )

    def test_create_student(self):
        student = Student.objects.create(
            user=self.user,
            student_id='12345',
            department='Computer Science',
            year_of_study=1
        )
        self.assertEqual(student.student_id, '12345')
        self.assertEqual(str(student), 'Student User - 12345')

class LecturerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='lecturer@example.com',
            username='lecturer',
            first_name='Lecturer',
            last_name='User',
            password='password123'
        )

    def test_create_lecturer(self):
        lecturer = Lecturer.objects.create(
            user=self.user,
            employee_id='L001',
            department='Computer Science',
            qualification='PhD'
        )
        self.assertEqual(lecturer.employee_id, 'L001')
        self.assertEqual(str(lecturer), 'Lecturer User - L001')
