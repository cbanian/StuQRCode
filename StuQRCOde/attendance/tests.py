from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, datetime, timedelta
import uuid
from .models import QRCode, AttendanceRecord, AttendanceStatistics
from accounts.models import Student, Lecturer
from courses.models import Course, Semester, ClassSchedule

User = get_user_model()

class QRCodeModelTest(TestCase):
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

    def test_create_qr_code(self):
        now = timezone.now()
        qr_code = QRCode.objects.create(
            course=self.course,
            valid_from=now,
            valid_until=now + timedelta(hours=1),
            is_active=True,
            created_by=self.lecturer
        )
        self.assertTrue(qr_code.is_valid)
        self.assertEqual(qr_code.days_remaining, 0)  # since it's 1 hour

class AttendanceRecordModelTest(TestCase):
    def setUp(self):
        self.lecturer_user = User.objects.create_user(
            email='lecturer@example.com',
            username='lecturer',
            first_name='Lecturer',
            last_name='User',
            password='password123'
        )
        self.lecturer = Lecturer.objects.create(
            user=self.lecturer_user,
            employee_id='L001',
            department='Computer Science',
            qualification='PhD'
        )
        self.student_user = User.objects.create_user(
            email='student@example.com',
            username='student',
            first_name='Student',
            last_name='User',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            student_id='12345',
            department='Computer Science',
            year_of_study=1
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
        self.schedule = ClassSchedule.objects.create(
            course=self.course,
            day='Monday',
            start_time=time(9, 0),
            end_time=time(10, 30),
            room='Room 101'
        )
        self.qr_code = QRCode.objects.create(
            course=self.course,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(hours=1),
            is_active=True,
            created_by=self.lecturer
        )

    def test_create_attendance_record(self):
        record = AttendanceRecord.objects.create(
            student=self.student,
            course=self.course,
            qr_code=self.qr_code,
            date=date.today(),
            time_in=timezone.now(),
            status='present',
            marked_by='qr_scan'
        )
        self.assertEqual(record.status, 'present')
        self.assertEqual(str(record), f'Student User - CS101 - {date.today()}')

class AttendanceStatisticsModelTest(TestCase):
    def setUp(self):
        self.lecturer_user = User.objects.create_user(
            email='lecturer@example.com',
            username='lecturer',
            first_name='Lecturer',
            last_name='User',
            password='password123'
        )
        self.lecturer = Lecturer.objects.create(
            user=self.lecturer_user,
            employee_id='L001',
            department='Computer Science',
            qualification='PhD'
        )
        self.student_user = User.objects.create_user(
            email='student@example.com',
            username='student',
            first_name='Student',
            last_name='User',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            student_id='12345',
            department='Computer Science',
            year_of_study=1
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

    def test_create_attendance_statistics(self):
        stats = AttendanceStatistics.objects.create(
            student=self.student,
            course=self.course,
            total_classes=10,
            attended_classes=8
        )
        self.assertEqual(stats.calculate_percentage(), 80.00)
        self.assertEqual(str(stats), 'Student User - CS101 - 80.00%')
