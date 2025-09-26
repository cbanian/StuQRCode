#!/usr/bin/env python
"""
Script to fix QR code URL generation for mobile access
This script provides utilities to generate QR codes with proper IP addresses
for mobile device access instead of localhost (127.0.0.1)
"""

import socket
import os
import sys

# Add the project to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StuQRCOde.settings')
import django
django.setup()

from django.conf import settings

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 8000))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # Fallback to localhost if unable to determine
        return "127.0.0.1"

def get_server_url():
    """Get the server URL for mobile access"""
    local_ip = get_local_ip()
    port = 8000  # Default Django development server port
    return f"http://{local_ip}:{port}"

def print_setup_instructions():
    """Print instructions for setting up mobile access"""
    local_ip = get_local_ip()
    server_url = get_server_url()
    
    print("=" * 60)
    print("QR CODE MOBILE ACCESS SETUP")
    print("=" * 60)
    print(f"Your computer's local IP address: {local_ip}")
    print(f"Server URL for mobile devices: {server_url}")
    print()
    print("To access your Django app from mobile devices:")
    print("1. Make sure your computer and mobile device are on the same WiFi network")
    print("2. Run the Django server with: python manage.py runserver 0.0.0.0:8000")
    print("3. On your mobile device, scan QR codes using this URL format:")
    print(f"   {server_url}/attendance/scan/<qr_code_id>/")
    print()
    print("To update your Django settings for mobile access:")
    print("Add these settings to your StuQRCOde/settings.py:")
    print(f"ALLOWED_HOSTS = ['{local_ip}', 'localhost', '127.0.0.1']")
    print("=" * 60)

if __name__ == "__main__":
    print_setup_instructions()
