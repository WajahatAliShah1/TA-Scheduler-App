from django.test import TestCase, Client
from TAScheduler.models import *


class TestCreateLab(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None
    course = None
    lab = None

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

        self.course = Course.objects.create(courseID=1, name="Software Engineering",
                                            location="EMS 180", hours="12:00 PM - 01:00 PM", days="M, W",
                                            instructor=self.instructor)
        self.course2 = Course.objects.create(courseID=2, name="Systems Programming",
                                             location="Chem 180", hours="12:00 PM - 01:00 PM", days="T, Th",
                                             instructor=self.instructor)

        self.course.TAs.add(self.TA)
        self.course2.TAs.add(self.TA)
        self.lab = Lab.objects.create(labID=1, name="Lab", location="EMS 280",
                                      hours="03:00 PM - 04:00 PM", days="M, W", course=self.course, TA=self.TA)

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_duplicateLab(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 1, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_blankID(self):
        r = self.dummyClient.post('/create_lab/', {"labID": "", "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when duplicate Lab was created")

    def test_blankName(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_blankLocation(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_blankHours(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_invalidHours(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "invalid input", "days": "M, W",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_blankDays(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_invalidDays(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "invalid input",
                                                   "course": self.course, "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: 'Software Engineering'",
                         "An error message was not displayed when duplicate Lab was created")

    def test_courseNotExisting(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 2, "labName": "Lab", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": "", "TA": self.TA})
        self.assertEqual(r.context["error"],
                         "Lab section was not created. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when duplicate Lab was created")

    def test_createLab(self):
        r = self.dummyClient.post('/create_lab/', {"labID": 10, "labName": "Lab2", "labLocation": "EMS 280",
                                                   "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                   "course": self.course2, "TA": self.TA})

        self.assertNotEqual(Lab.objects.get(labID=1), {"labID": 10, "labName": "Lab2", "labLocation": "EMS 280",
                                                       "labHours": "03:00 PM - 04:00 PM", "days": "M, W",
                                                       "course": self.course2, "TA": self.TA},
                            "Lab was not created successfully")
