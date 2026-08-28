import unittest
import requests


def print_log(*texts):
    with open("event_logs.txt", "a") as file_object:
        for text in texts:
            file_object.write(str(text) + " ")
        file_object.write("\n")


class Test(unittest.TestCase):

    def test_get_employee_dept(self):
        try:
            result = requests.get("http://0.0.0.0:8000/employees/employee/Finance")
            self.assertEqual(result.status_code, 200)
            self.assertIsNotNone(result.content, None)
            print_log("test_get_employee_dept: Success")
        except requests.exceptions.ConnectionError:
            print('connection error occurred')
            print_log("test_get_employee_dept: ConnectionError")

    def test_get_all_employess_for_dept(self):
        try:
            required = {
                'status': 'Success',
                'employees': [
                    {
                        'first_name': 'Prajwal',
                        'last_name': 'SS',
                        'emp_id': 8,
                        'address': 'Mangalore',
                        'mobile': '9847588659',
                        'dept': 'Finance',
                        'salary': 120000,
                        
                    }
                ]
            }

            result = requests.get("http://0.0.0.0:8000/employees/employee/8")
            self.assertEqual(result.status_code, 200)
            result = result.json()
            print_log("test_get_all_employees_for_dept: Success")

        except requests.exceptions.ConnectionError:
            print('connection error occurred')
            print_log("test_get_all_emplyees_for_dept: ConnectionError")


if __name__ == '__main__':
    unittest.main()
