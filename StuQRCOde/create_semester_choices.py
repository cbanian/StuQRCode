#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StuQRCOde.settings')
django.setup()

from courses.models import Semester
from datetime import date

def create_semester_choices():
    """Create semester choices like Semester 1, Semester 2, etc."""
    
    # Delete existing semesters
    Semester.objects.all().delete()
    
    # Create semester choices
    semesters = [
        {
            'name': 'Semester 1',
            'year': 2025,
            'start_date': date(2025, 1, 15),
            'end_date': date(2025, 5, 15),
            'is_active': True
        },
        {
            'name': 'Semester 2',
            'year': 2025,
            'start_date': date(2025, 8, 15),
            'end_date': date(2025, 12, 15),
            'is_active': False
        }
    ]
    
    for semester_data in semesters:
        semester, created = Semester.objects.get_or_create(
            name=semester_data['name'],
            year=semester_data['year'],
            defaults=semester_data
        )
        if created:
            print(f"Created semester: {semester}")
        else:
            print(f"Semester already exists: {semester}")
            # Update existing semester with new data
            for key, value in semester_data.items():
                setattr(semester, key, value)
            semester.save()
            print(f"Updated semester: {semester}")

if __name__ == "__main__":
    create_semester_choices()
    print("Semester choices created successfully!")
