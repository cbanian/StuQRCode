from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from .models import Semester, Course, ClassSchedule
from accounts.models import Lecturer

User = get_user_model()

class SemesterModelTest(TestCase):
    def test_create_semester(self):
        semester = Semester.objects.create(
            name='Fall',
            year=2023,
            start_date=date(2023, 9, 1),
            end_date=date(2023, 12, 31),
            is_active=True
        )
        self.assertEqual(str(semester), 'Fall 2023')
        self.assertTrue(semester.is_active)

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='lecturer@example.com',
            username='lecturer',
            first_name='Lecturer',
            last_name='User',
            password='password123'
        )
        self.lecturer = Lecturer.objects.create(
            user=self.user,
            employee_id='L001',
            department='Computer Science',
            qualification='PhD'
        )
        self.semester = Semester.objects.create(
            name='Fall',
            year=2023,
            start_date=date(2023, 9, 1),
            end_date=date(2023, 12, 31)
        )

    def test_create_course(self):
        course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            description='Basic course',
            credit_hours=3,
            lecturer=self.lecturer,
            semester=self.semester
        )
        self.assertEqual(course.code, 'CS101')
        self.assertEqual(str(course), 'CS101 - Introduction to Computer Science')

class ClassScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='lecturer@example.com',
            username='lecturer',
            first_name='Lecturer',
            last_name='User',
            password='password123'
        )
        self.lecturer = Lecturer.objects.create(
            user=self.user,
            employee_id='L001',
            department='Computer Science',
            qualification='PhD'
        )
        self.semester = Semester.objects.create(
            name='Fall',
            year=2023,
            start_date=date(2023, 9, 1),
            end_date=date(2023, 12, 31)
        )
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            description='Basic course',
            credit_hours=3,
            lecturer=self.lecturer,
            semester=self.semester
        )

    def test_create_class_schedule(self):
        schedule = ClassSchedule.objects.create(
            course=self.course,
            day='Monday',
            start_time=time(9, 0),
            end_time=time(10, 30),
            room='Room 101'
        )
        self.assertEqual(schedule.day, 'Monday')
        self.assertEqual(str(schedule), 'CS101 - Monday 09:00:00-10:30:00')
