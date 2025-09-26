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

def update_qr_for_testing():
    now = timezone.now()

    # Find the most recently created QR code
    try:
        qr = QRCode.objects.order_by('-created_at').first()

        if not qr:
            print("No QR codes found in database.")
            return

        print(f"Found QR code: {qr.id}")
        print(f"Course: {qr.course.name}")
        print(f"Current valid_from: {qr.valid_from}")
        print(f"Current valid_until: {qr.valid_until}")
        print(f"Current is_valid: {qr.is_valid}")
        print(f"Current time: {now}")

        # Update to make it valid for the next hour
        qr.valid_from = now
        qr.valid_until = now + timedelta(hours=1)
        qr.save()

        print("\n--- UPDATED ---")
        print(f"New valid_from: {qr.valid_from}")
        print(f"New valid_until: {qr.valid_until}")
        print(f"New is_valid: {qr.is_valid}")

        print("\n--- TEST INSTRUCTIONS ---")
        print("1. Start your Django server: python manage.py runserver")
        print("2. Go to: http://localhost:8000/attendance/qr-codes/{}/".format(qr.id))
        print("3. The QR code should now display properly instead of showing 'QR Code Expired'")
        print("4. You can also test the download button")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    update_qr_for_testing()
