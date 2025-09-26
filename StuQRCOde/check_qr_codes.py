#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StuQRCOde.settings')
sys.path.append('.')
django.setup()

from attendance.models import QRCode
from django.utils import timezone

def check_qr_codes():
    now = timezone.now()
    print(f"Current time: {now}")
    print(f"Current timezone: {now.tzinfo}")

    qrs = QRCode.objects.all()
    print(f"Total QR codes: {qrs.count()}")

    for qr in qrs:
        print(f"\nQR Code ID: {qr.id}")
        print(f"  Course: {qr.course.name} ({qr.course.code})")
        print(f"  Valid from: {qr.valid_from}")
        print(f"  Valid until: {qr.valid_until}")
        print(f"  Is active: {qr.is_active}")
        print(f"  Is valid: {qr.is_valid}")
        print(f"  Created at: {qr.created_at}")

        # Check why it's invalid
        if not qr.is_active:
            print("  Reason: QR code is not active")
        elif qr.valid_from > now:
            print(f"  Reason: Valid from date ({qr.valid_from}) is in the future")
        elif qr.valid_until < now:
            print(f"  Reason: Valid until date ({qr.valid_until}) has passed")
        else:
            print("  Reason: Should be valid")

if __name__ == '__main__':
    check_qr_codes()
