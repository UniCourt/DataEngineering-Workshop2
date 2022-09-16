import unittest
import requests


def print_log( *texts ):
    with open("event_logs.txt", "a") as file_object:
        for text in texts:
            file_object.write(str(text) + " ")
        file_object.write("\n")


class Test(unittest.TestCase):

    def test_get_student_branch(self):
        result = requests.get("http://0.0.0.0:8000/members/rest/student/B.COM")
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result, None)

    def test_get_all_students_for_branch(self):
        required = {'status': 'success',
                    'students': [{'address': 'sdgsg',
                                  'branch': 'B.COM',
                                  'first_name': 'shamith',
                                  'last_name': 'Shetty',
                                  'mobile': '9008809863',
                                  'roll_number': 1}]}

        result = requests.get("http://0.0.0.0:8000/members/rest/student/1")
        self.assertEqual(result.status_code, 200)

        result = result.json()
        self.assertEqual(result, required)
