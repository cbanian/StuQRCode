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

def fix_qr_validity():
    now = timezone.now()

    # Find QR codes that are not valid
    invalid_qrs = QRCode.objects.filter(is_valid=False)

    if not invalid_qrs.exists():
        print("No invalid QR codes found.")
        return

    print(f"Found {invalid_qrs.count()} invalid QR codes.")
    print(f"Current time: {now}")

    # Update the first invalid QR code to be valid
    qr = invalid_qrs.first()

    print(f"\nUpdating QR Code: {qr.id}")
    print(f"Course: {qr.course.name}")
    print(f"Original valid_from: {qr.valid_from}")
    print(f"Original valid_until: {qr.valid_until}")

    # Set valid_from to now and valid_until to 1 hour from now
    qr.valid_from = now
    qr.valid_until = now + timedelta(hours=1)
    qr.save()

    print(f"Updated valid_from: {qr.valid_from}")
    print(f"Updated valid_until: {qr.valid_until}")
    print(f"Is valid now: {qr.is_valid}")

    print(f"\nQR Code {qr.id} is now valid for the next hour.")
    print(f"You can test the QR code display at: /attendance/qr-codes/{qr.id}/")

if __name__ == '__main__':
    fix_qr_validity()
