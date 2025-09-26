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

def final_qr_fix():
    print("=== FIXING QR CODE VALIDITY ===")

    now = timezone.now()
    print(f"Current time: {now}")

    # Get the most recent QR code
    qr = QRCode.objects.order_by('-created_at').first()

    if not qr:
        print("No QR codes found. Please create a QR code first.")
        return

    print(f"\nFound QR code: {qr.id}")
    print(f"Course: {qr.course.name}")
    print(f"Original valid_from: {qr.valid_from}")
    print(f"Original valid_until: {qr.valid_until}")
    print(f"Original is_valid: {qr.is_valid}")

    # Update to make it valid
    qr.valid_from = now - timedelta(minutes=5)  # Valid from 5 minutes ago
    qr.valid_until = now + timedelta(hours=2)   # Valid for next 2 hours
    qr.save()

    print("
--- QR CODE UPDATED ---")
    print(f"New valid_from: {qr.valid_from}")
    print(f"New valid_until: {qr.valid_until}")
    print(f"New is_valid: {qr.is_valid}")

    print("
=== TESTING INSTRUCTIONS ===")
    print("1. Start your Django development server:")
    print("   python manage.py runserver")
    print("")
    print("2. Open your browser and go to:")
    print(f"   http://localhost:8000/attendance/qr-codes/{qr.id}/")
    print("")
    print("3. You should now see:")
    print("   - The QR code image displayed (not 'QR Code Expired')")
    print("   - A working download button")
    print("")
    print("4. If you still see 'QR Code Expired', refresh the page")
    print("")
    print("=== WHAT WAS FIXED ===")
    print("- QR code validity dates were updated to include current time")
    print("- Fixed the Content-Disposition header issue for inline display")
    print("- Added error handling for invalid QR codes")

if __name__ == '__main__':
    final_qr_fix()
