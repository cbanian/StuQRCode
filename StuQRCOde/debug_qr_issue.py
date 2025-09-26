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

def debug_qr_issue():
    print("=== QR CODE DEBUG INFORMATION ===")

    now = timezone.now()
    print(f"Current time: {now}")
    print(f"Timezone: {now.tzinfo}")

    qrs = QRCode.objects.all().order_by('-created_at')

    print(f"\nTotal QR codes in database: {qrs.count()}")

    if qrs.count() == 0:
        print("No QR codes found. You need to create a QR code first.")
        return

    print("\n=== ALL QR CODES ===")
    for i, qr in enumerate(qrs, 1):
        print(f"\n{i}. QR Code ID: {qr.id}")
        print(f"   Course: {qr.course.name} ({qr.course.code})")
        print(f"   Valid from: {qr.valid_from}")
        print(f"   Valid until: {qr.valid_until}")
        print(f"   Is active: {qr.is_active}")
        print(f"   Is valid: {qr.is_valid}")
        print(f"   Created: {qr.created_at}")

        # Check why it's invalid
        if not qr.is_active:
            print("   Status: INACTIVE")
        elif qr.valid_from > now:
            print("   Status: NOT YET VALID")
        elif qr.valid_until < now:
            print("   Status: EXPIRED")
        else:
            print("   Status: VALID ✓")

    # Find the most recent QR code
    latest_qr = qrs.first()
    print("
=== MOST RECENT QR CODE ===")
    print(f"ID: {latest_qr.id}")
    print(f"URL: /attendance/qr-codes/{latest_qr.id}/")
    print(f"Is valid: {latest_qr.is_valid}")

    if latest_qr.is_valid:
        print("✓ This QR code should display properly!")
    else:
        print("❌ This QR code will show 'QR Code Expired'")
        print("To fix this, you need to update the validity dates.")

    print("
=== NEXT STEPS ===")
    print("1. If you want to test with the current QR code, update its validity dates")
    print("2. Or create a new QR code with valid dates")
    print("3. Then visit the QR code detail page to test the display")

if __name__ == '__main__':
    debug_qr_issue()
