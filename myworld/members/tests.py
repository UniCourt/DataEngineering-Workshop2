import json
from django.test import Client, TestCase
from members.models import Blog, Employee, Students


class MemberAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = Students.objects.create(
            first_name="Shamith",
            last_name="H",
            address="MK",
            roll_number=1,
            mobile="8976543540",
            branch="CA",
        )

    def test_get_student_branch(self):
        response = self.client.get("/members/rest/student/CA")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "success")

    def test_employee_crud(self):
        # 1. Create
        emp_data = {
            "emp_id": 101,
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "department": "IT",
            "salary": 60000.00,
        }
        res = self.client.post("/members/rest/employee/", data=emp_data)
        self.assertIn(res.status_code, [200, 201])

        # 2. Read
        res = self.client.get("/members/rest/employee/101")
        self.assertEqual(res.status_code, 200)

        # 3. Update salary
        res = self.client.put(
            "/members/rest/employee/101",
            data=json.dumps({"salary": 70000.00}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)

        # 4. Delete
        res = self.client.delete("/members/rest/employee/101")
        self.assertEqual(res.status_code, 200)
