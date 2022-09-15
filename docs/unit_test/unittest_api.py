import unittest
import requests


def print_log( *texts ):
    with open("event_logs.txt", "a") as file_object:
        for text in texts:
            file_object.write(str(text) + " ")
        file_object.write("\n")


class Test(unittest.TestCase):

    def test_get_student_branch(self):
        result = requests.get("http://localhost:8000/rest/student/")
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result, None)

    def test_get_all_students_for_branch(self):
        required = {
                "id": 1,
                "article": {
                    "Error": "No article found with the id 1"
                }
            }

        result = requests.get("http://localhost:8000/rest/article/60")
        self.assertNotEqual(result, None)
        self.assertEqual(result.status_code, 200)

        result = requests.get("http://localhost:8000/rest/article/1")
        self.assertEqual(result.status_code, 200)

        result = result.json()
        self.assertEqual(result, required)
