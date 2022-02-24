from django.test import TestCase, Client
from TAScheduler.models import *


class TestCreateCourse(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None
    course = None

    def setUp(self):
        self.dummyClient = Client()
        self.TA = UserProfile.objects.create(userID=1, userType="TA", username="TA1"
                                             , password="TA123", name="TA Dummy", address="TA Address",
                                             phone=3234457876, email="TAEmail@email.com")

        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Instructor1"
                                                     , password="Instructor123", name="Instructor Dummy",
                                                     address="Instructor Address", phone=3234457176,
                                                     email="InstructorEmail@email.com")

        self.admin = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="Admin1"
                                                , password="Admin123", name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.course = Course.objects.create(courseID=1, name="Test Course", location="location",
                                            hours="10:00 AM - 10:50 AM", days="M, W, F", instructor=self.instructor)

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_duplicateCourse(self):
        r = self.dummyClient.post('/create_course/', {"ID": 1, "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def test_blankID(self):
        r = self.dummyClient.post('/create_course/', {"ID": "", "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"], "Course was not created. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when name was left blank")

    def test_blankName(self):
        r = self.dummyClient.post('/create_course/', {"ID": 2, "name": "",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def test_blankLocation(self):
        r = self.dummyClient.post('/create_course/', {"ID": 2, "name": "Systems Programming",
                                                      "location": "", "hours": "12:00PM - 01:00PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def test_blankHours(self):
        r = self.dummyClient.post('/create_course/', {"ID": 2, "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def test_invalidHours(self):
        r = self.dummyClient.post('/create_course/', {"ID": 2, "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "invalid input",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def test_blankDays(self):
        r = self.dummyClient.post('/create_course/', {"ID": 2, "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "", "instructor": self.instructor})

        self.assertEqual(r.context["error"],
                         "Course was not created. invalid literal for int() with base 10: 'Instructor1'",
                         "An error message was not displayed when name was left blank")

    def createCourse(self):
        r = self.dummyClient.post('/create_course/', {"courseID": 99, "name": "Software Engineering",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(Course.objects.get(courseID=1), Course(courseID=99, name="Software Engineering", location="EMS 180", hours="12:00 PM - 01:00 PM", days="M, W", instructor=self.instructor), "Course was not created successfully")

    def createCourseWTA(self):
        r = self.dummyClient.post('/create_course/', {"courseID": 100, "name": "Systems Programming",
                                                      "location": "EMS 180", "hours": "12:00 PM - 01:00 PM",
                                                      "days": "M, W", "instructor": self.instructor})

        self.assertEqual(Course.objects.get(courseID=1),
                         Course(courseID=99, name="Software Engineering", location="EMS 180",
                                hours="12:00 PM - 01:00 PM", days="M, W", instructor=self.instructor),
                         "Course was not created successfully")
        course = Course.objects.get(courseID=2)
        course.TAs.add(self.TA)
        course.save()
        self.assertEqual(Course.objects.get(courseID=2).TAs[0], self.TA)
