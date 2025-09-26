#!/usr/bin/env python
import os
import sys
import django
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StuQRCOde.settings')
sys.path.append('.')
django.setup()

from attendance.models import QRCode
from django.utils import timezone

def update_existing_qr():
    print("UPDATING EXISTING QR CODE VALIDITY...")

    now = timezone.now()
    print(f"Current time: {now}")

    # Get the most recent QR code
    qr = QRCode.objects.order_by('-created_at').first()

    if not qr:
        print("ERROR: No QR codes found in database!")
        return

    print(f"\nFound QR code ID: {qr.id}")
    print(f"Course: {qr.course.name}")
    print(f"Before update - Is valid: {qr.is_valid}")

    # Update validity dates
    qr.valid_from = now - timedelta(minutes=10)  # Valid from 10 minutes ago
    qr.valid_until = now + timedelta(hours=24)   # Valid for next 24 hours
    qr.is_active = True
    qr.save()

    print("
UPDATED SUCCESSFULLY!")
    print(f"New valid_from: {qr.valid_from}")
    print(f"New valid_until: {qr.valid_until}")
    print(f"New is_valid: {qr.is_valid}")

    print("
TEST THE QR CODE:")
    print("1. Start server: python manage.py runserver")
    print("2. Visit: http://localhost:8000/attendance/qr-codes/{}/".format(qr.id))
    print("3. QR code should display properly now!")

if __name__ == '__main__':
    update_existing_qr()
