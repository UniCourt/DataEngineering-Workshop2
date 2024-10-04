from django.test import TestCase
from .models import Students
import requests

# Create your tests here.
class StudentsModelTests(TestCase):
    def test_create_student(self):
        required = {'status': 'success',
                    'students': [{'address': 'Mallikatte',
                                  'branch': 'BA',
                                  'first_name': 'Vyasa M',
                                  'last_name': 'Nayak',
                                  'mobile': '9141592653',
                                  'roll_number': 186}]}

        Students.objects.create(
            first_name = "Vyasa M",
            last_name = "Nayak",
            address = "Mallikatte",
            roll_number = 186,
            mobile = "9141592653",
            branch = "BA"
        )

        result = requests.get("http://0.0.0.0:8000/members/rest/student/186")
        self.assertEqual(result.status_code, 200)

        result = result.json()
        self.assertEqual(result, required)