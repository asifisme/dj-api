"""
Generate dummy user data for testing (Django fixture format)
"""

import sys
import os
import django
import uuid
import json
from faker import Faker
from datetime import datetime
from django.contrib.auth.hashers import make_password

# Add Django root directory (the one containing manage.py) to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xApi.settings')

# Setup Django
django.setup()

# Import the model after Django is initialized
from xApiAuthentication.models import CustomUser

# Faker instance
fake = Faker()

fixture_data = []
num = 100 

common_password = make_password('password')

for i in range(1000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = str(num + i) 
    email = fake.unique.email()
    phn_num = fake.phone_number()
    gender = fake.random_element(elements=('Male', 'Female'))
    dt_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60)
    uid = uuid.uuid4().hex[:32].lower()

    fixture_data.append({
        'model': 'xApiAuthentication.customuser',
        'pk': i + 1,
        'fields': {
            'password': common_password,
            'last_login': None,
            'is_superuser': False,
            'username': str(num + i),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phn_num': phn_num,
            'gender': gender,
            'dt_of_birth': str(dt_of_birth),
            'uid': uid,
            'pro_photo': None,
            'is_staff': False,
            'is_active': True,
            'date_joined': datetime.now().isoformat(),
            'groups': [],
            'user_permissions': []
        }
    })

# Output file path
output_file = os.path.join(os.path.dirname(__file__), 'user.json')

# Write fixture to file
with open(output_file, 'w') as f:
    json.dump(fixture_data, f, indent=4)

print(f'✅ Generated {len(fixture_data)} user fixtures in \"{output_file}\"')
