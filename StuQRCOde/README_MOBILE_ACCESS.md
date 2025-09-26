# Mobile Access Configuration for StuQRCOde

## Current Network Configuration
- **Local IP Address**: 192.168.1.115
- **Server URL**: http://192.168.1.115:8000

## Setup Instructions

### 1. Start Django Server for Mobile Access
```bash
python manage.py runserver 0.0.0.0:8000
```

### 2. Mobile Device Setup
1. Connect your mobile device to the **same WiFi network** as your computer
2. Open your mobile browser
3. Navigate to: http://192.168.1.115:8000

### 3. QR Code Scanning URLs
For attendance scanning, use these URL formats:
- **Base URL**: http://192.168.1.115:8000
- **QR Code Scanning**: http://192.168.1.115:8000/attendance/scan/<qr_code_id>/

### 4. Testing Mobile Access
1. Ensure your computer's firewall allows incoming connections on port 8000
2. Test connectivity by opening http://192.168.1.115:8000 on your mobile browser
3. You should see the StuQRCOde landing page

### 5. Troubleshooting
- **Connection refused**: Check if Windows Firewall is blocking port 8000
- **Page not loading**: Verify both devices are on the same network
- **Invalid QR code**: Ensure the QR code contains the full URL with your IP address

## Security Note
This configuration is for development/testing purposes only. In production, use proper domain names and HTTPS.
