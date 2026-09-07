import json
import os
import sys
import unittest

# Setup Django environment for standalone unittest execution
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myworld.settings")
import django

django.setup()

from django.test import Client
from members.models import Blog, Employee, Students


class TestRESTAPI(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        # Clean up database tables before test
        Students.objects.all().delete()
        Employee.objects.all().delete()
        Blog.objects.all().delete()

        # Create sample student
        self.student = Students.objects.create(
            first_name="Shamith",
            last_name="H",
            address="MK",
            roll_number=1,
            mobile="8976543540",
            branch="CA",
        )

    def test_get_student_branch(self):
        """Test getting student by branch."""
        response = self.client.get("/members/rest/student/CA")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(len(data.get("students", [])) > 0)

    def test_get_all_students_for_branch(self):
        """Test getting student by roll number."""
        response = self.client.get("/members/rest/student/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data["students"][0]["roll_number"], 1)

    def test_post_add_student(self):
        """Test adding a new student via POST."""
        post_data = {
            "first_name": "Rohan",
            "last_name": "Kumar",
            "address": "Bangalore",
            "roll_number": 2,
            "mobile": "9876543210",
            "branch": "MBA",
        }
        response = self.client.post("/members/rest/student/", data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Students.objects.filter(roll_number=2).exists())

    def test_employee_crud(self):
        """Test Employee APIs: Create, Read, Update salary, Delete."""
        # 1. Add Employee (POST)
        emp_data = {
            "emp_id": 101,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "department": "Engineering",
            "salary": 75000.00,
        }
        response = self.client.post("/members/rest/employee/", data=emp_data)
        self.assertIn(response.status_code, [200, 201])

        # 2. Get Employee by emp_id (GET)
        response = self.client.get("/members/rest/employee/101")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data["employee"]["emp_id"], 101)

        # 3. Update Employee Salary (PUT / PATCH)
        update_data = json.dumps({"salary": 85000.00})
        response = self.client.put(
            "/members/rest/employee/101",
            data=update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        emp = Employee.objects.get(emp_id=101)
        self.assertEqual(float(emp.salary), 85000.00)

        # 4. Delete Employee by emp_id (DELETE)
        response = self.client.delete("/members/rest/employee/101")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Employee.objects.filter(emp_id=101).exists())

    def test_blog_scraping_api(self):
        """Test Blog REST API and Blog creation."""
        blog = Blog.objects.create(
            title="Test Python Blog",
            author="Python Dev",
            release_date="2026-08-25",
            blog_time="10:00:00",
            total_comments=2,
            recommended_google=5,
            html_file_path="/tmp/test.html",
        )
        response = self.client.get("/members/rest/blog/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(len(data.get("blogs", [])) > 0)


if __name__ == "__main__":
    with open("event_logs.txt", "w") as log_file:
        runner = unittest.TextTestRunner(stream=log_file, verbosity=2)
        result = unittest.main(testRunner=runner, exit=False)
