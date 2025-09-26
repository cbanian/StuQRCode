st#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StuQRCOde.settings')
sys.path.append('.')
django.setup()

from attendance.models import QRCode
from django.utils import timezone

def test_qr_display():
    now = timezone.now()
    print(f"Current time: {now}")

    # Get all QR codes
    qrs = QRCode.objects.all().order_by('-created_at')

    print(f"\nTotal QR codes: {qrs.count()}")
    print("\nQR Code Status:")

    for qr in qrs:
        status = "VALID" if qr.is_valid else "INVALID"
        print(f"\nID: {qr.id}")
        print(f"Course: {qr.course.name} ({qr.course.code})")
        print(f"Valid from: {qr.valid_from}")
        print(f"Valid until: {qr.valid_until}")
        print(f"Status: {status}")
        print(f"Test URL: /attendance/qr-codes/{qr.id}/")

        if qr.is_valid:
            print("✓ This QR code should display properly!")
            break

    # If no valid QR codes, suggest creating one
    valid_count = sum(1 for qr in qrs if qr.is_valid)
    if valid_count == 0:
        print("\n❌ No valid QR codes found.")
        print("To test QR code display, you need a QR code with:")
        print("- valid_from <= current time")
        print("- valid_until >= current time")
        print("- is_active = True")

if __name__ == '__main__':
    test_qr_display()
