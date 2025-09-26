#!/usr/bin/env python
"""
Setup script for Student Registration & Attendance Web Application
"""

import os
import sys
import subprocess

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Student Registration & Attendance System Setup")
    print("=" * 60)
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("⚠ Warning: Virtual environment not detected")
        print("Please activate your virtual environment first:")
        print("  Windows: venv\\Scripts\\activate")
        print("  Linux/Mac: source venv/bin/activate")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return
    
    # Create superuser
    print("\nCreating superuser...")
    print("You will be prompted to create an admin account")
    response = input("Create superuser now? (y/n): ")
    if response.lower() == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo start the development server:")
    print("  python manage.py runserver")
    print("\nAccess the application at:")
    print("  http://localhost:8000/")
    print("  Admin panel: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
