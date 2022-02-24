from django.test import TestCase, Client
from TAScheduler.models import *


class test_editLab(TestCase):
    def setUp(self):
        self.supervisor = UserProfile.objects.create(userID=1, userType="SUPERVISOR", username="supervisor",
                                                     name="supervisor", address="address", phone=9876543212,
                                                     email="email@email.com")
        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="instructor1",
                                                     name="instructor", address="address", phone=1234567890,
                                                     email="email@email.com")
        self.TA = UserProfile.objects.create(userID=3, userType="TA", username="ta", name="ta", address="address",
                                             phone=2123456789, email="email@email.com")
        self.testCourse = Course.objects.create(courseID=1, name="Test Course", location="location",
                                                hours="10:00 AM - 10:50 AM", days="M, W, F", instructor=self.instructor)
        self.testCourse2 = Course.objects.create(courseID=2, name="Test Course 2", location="location",
                                                 hours="10:00 AM - 10:50 AM", days="M, W, F",
                                                 instructor=self.instructor)
        self.testCourse.TAs.add(self.TA)
        self.testCourse2.TAs.add(self.TA)
        self.testLab = Lab.objects.create(labID=1, name="Test Lab", location="location", hours="10:00 AM - 11:50 AM",
                                          days="M, W, F", course=self.testCourse, TA=self.TA)
        self.client = Client()
        self.client.session["user_id"] = self.instructor.userID
        self.client.post("/", {"useraccount": self.supervisor.username, "password": self.supervisor.password})

    def test_editName(self):
        self.client.post("/edit_lab/",
                         {"name": "new name", "location": self.testLab.location, "hours": self.testLab.hours,
                          "days": self.testLab.days, "course": self.testLab.course.courseID,
                          "TA": self.testLab.TA.userID,
                          "submit": self.testLab.labID})
        self.assertEqual("new name", Lab.objects.get(labID=self.testLab.labID).name,
                         "Lab name was not set correctly")

    def test_editBlankName(self):
        name = self.testLab.name
        resp = self.client.post("/edit_lab/",
                                {"name": "", "location": self.testLab.location, "hours": self.testLab.hours,
                                 "days": self.testLab.days, "course": self.testLab.course.courseID,
                                 "TA": self.testLab.TA.userID,
                                 "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"], "Lab section was not changed. Name should not be left blank",
                         "An error message was not displayed when name was left blank")
        self.assertEqual(name, Lab.objects.get(labID=self.testLab.labID).name,
                         "Name was changed when it shouldn't have been")

    def test_editLocation(self):
        self.client.post("/edit_lab/",
                         {"name": self.testLab.name, "location": "new location", "hours": self.testLab.hours,
                          "days": self.testLab.days, "course": self.testLab.course.courseID,
                          "TA": self.testLab.TA.userID,
                          "submit": self.testLab.labID})
        self.assertEqual("new location", Lab.objects.get(labID=self.testLab.labID).location,
                         "Lab location was not set correctly")

    def test_editBlankLocation(self):
        location = self.testLab.location
        resp = self.client.post("/edit_lab/",
                                {"name": self.testLab.name, "location": "", "hours": self.testLab.hours,
                                 "days": self.testLab.days, "course": self.testLab.course.courseID,
                                 "TA": self.testLab.TA.userID,
                                 "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"], "Lab section was not changed. Location should not be left blank",
                         "An error message was not displayed when location was left blank")
        self.assertEqual(location, Lab.objects.get(labID=self.testLab.labID).location,
                         "Location was changed when it shouldn't have been")

    def test_editHours(self):
        self.client.post("/edit_lab/",
                         {"name": self.testLab.name, "location": self.testLab.location, "hours": "11:00 AM - 12:00 PM",
                          "days": self.testLab.days, "course": self.testLab.course.courseID,
                          "TA": self.testLab.TA.userID,
                          "submit": self.testLab.labID})
        self.assertEqual("11:00 AM - 12:00 PM", Lab.objects.get(labID=self.testLab.labID).hours,
                         "Lab hours were not set correctly")

    def test_editBlankHours(self):
        hours = self.testLab.hours
        resp = self.client.post("/edit_lab/",
                                {"name": self.testLab.name, "location": self.testLab.location,
                                 "hours": "",
                                 "days": self.testLab.days, "course": self.testLab.course.courseID,
                                 "TA": self.testLab.TA.userID,
                                 "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"], "Lab section was not changed. Hours should not be left blank",
                         "An error message was not displayed when hours were left blank")
        self.assertEqual(hours, Lab.objects.get(labID=self.testLab.labID).hours,
                         "Hours were changed when they shouldn't have been")

    def test_editInvalidHours(self):
        hours = self.testLab.hours
        resp = self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                               "hours": "invalid input",
                                               "days": self.testLab.days, "course": self.testLab.course.courseID,
                                               "TA": self.testLab.TA.userID,
                                               "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"],
                         "Lab section was not changed. Wrong format for hours. Format should be HH:MM AM/PM - HH:MM "
                         "AM/PM",
                         "An error message was not displayed when hours entered incorrectly")
        self.assertEqual(hours, Lab.objects.get(labID=self.testLab.labID).hours,
                         "Hours were changed when they shouldn't have been")

    def test_editDays(self):
        self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                        "hours": self.testLab.hours,
                                        "days": "T, Th", "course": self.testLab.course.courseID,
                                        "TA": self.testLab.TA.userID,
                                        "submit": self.testLab.labID})
        self.assertEqual("T, Th", Lab.objects.get(labID=self.testLab.labID).days,
                         "Lab days were not set correctly")

    def test_editBlankDays(self):
        days = self.testLab.days
        resp = self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                               "hours": self.testLab.hours,
                                               "days": "", "course": self.testLab.course.courseID,
                                               "TA": self.testLab.TA.userID,
                                               "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"], "Lab section was not changed. At least one day must be selected",
                         "An error message was not displayed when the days were left unpicked")
        self.assertEqual(days, Lab.objects.get(labID=self.testLab.labID).days,
                         "Days were changed when they shouldn't have been")

    def test_editCourse(self):
        self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                        "hours": self.testLab.hours,
                                        "days": self.testLab.days, "course": self.testCourse2.courseID,
                                        "TA": self.testLab.TA.userID,
                                        "submit": self.testLab.labID})
        self.assertEqual(self.testCourse2, Lab.objects.get(labID=self.testLab.labID).course,
                         "Lab course was not set correctly")

    def test_editInvalidCourse(self):
        self.testCourse2.TAs.remove(self.TA)
        resp = self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                               "hours": self.testLab.hours,
                                               "days": self.testLab.days, "course": self.testCourse2.courseID,
                                               "TA": self.testLab.TA.userID,
                                               "submit": self.testLab.labID})
        self.assertEqual(resp.context["error"],
                         "Lab section was not changed. TAs cannot be assigned to labs for courses they are not "
                         "assigned to",
                         "An error message was not displayed when trying to assign a lab to a course that the TA is "
                         "not assigned to")
        self.assertEqual(self.testCourse, Lab.objects.get(labID=self.testLab.labID).course)

    def test_editTA(self):
        self.client.post("/edit_lab/", {"name": self.testLab.name, "location": self.testLab.location,
                                        "hours": self.testLab.hours, "days": self.testLab.days,
                                        "course": self.testLab.course, "TA": [self.TA.userID],
                                        "submit": self.testLab.labID})
        self.assertEqual(self.TA, Lab.objects.get(labID=self.testLab.labID).TA,
                         "Lab TA was not set correctly")
