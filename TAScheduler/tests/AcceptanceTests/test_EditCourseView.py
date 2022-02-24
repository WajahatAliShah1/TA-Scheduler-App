from django.test import TestCase, Client
from TAScheduler.models import *


class test_editCourse(TestCase):
    def setUp(self):
        self.instructor = UserProfile.objects.create(userID=1, userType="INSTRUCTOR", username="instructor1",
                                                     name="instructor", address="address", phone=1234567890,
                                                     email="email@email.com")
        self.newInstructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="instructor2",
                                                        name="instructor", address="address", phone=1234567890,
                                                        email="email@email.com")
        self.TA = UserProfile.objects.create(userID=3, userType="TA", username="ta", name="ta", address="address",
                                             phone=2123456789, email="email@email.com")
        self.testCourse = Course.objects.create(courseID=1, name="Test Course", location="location",
                                                hours="10:00 AM - 10:50 AM", days="M, W, F", instructor=self.instructor)
        self.client = Client()
        self.client.session["user_id"] = self.instructor.userID

    def test_editName(self):
        self.client.post("/edit_course/",
                         {"name": "new name", "location": self.testCourse.location, "hours": self.testCourse.hours,
                          "days": self.testCourse.days, "instructor": self.testCourse.instructor.userID,
                          "submit": self.testCourse.courseID})
        self.assertEqual("new name", Course.objects.get(courseID=self.testCourse.courseID).name,
                         "Course name was not set correctly")

    def test_editBlankName(self):
        name = self.testCourse.name
        resp = self.client.post("/edit_course/",
                                {"name": "", "location": self.testCourse.location, "hours": self.testCourse.hours,
                                 "days": self.testCourse.days, "instructor": self.testCourse.instructor.userID,
                                 "submit": self.testCourse.courseID})
        self.assertEqual(resp.context["error"], "Course was not edited. Name should not be left blank",
                         "An error message was not displayed when name was left blank")
        self.assertEqual(name, Course.objects.get(courseID=self.testCourse.courseID).name, "Name was changed when it "
                                                                                           "shouldn't have been")

    def test_editLocation(self):
        self.client.post("/edit_course/",
                         {"name": self.testCourse.name, "location": "new location", "hours": self.testCourse.hours,
                          "days": self.testCourse.days, "instructor": self.testCourse.instructor.userID,
                          "submit": self.testCourse.courseID})
        self.assertEqual("new location", Course.objects.get(courseID=self.testCourse.courseID).location,
                         "Course location was not set correctly")

    def test_editBlankLocation(self):
        location = self.testCourse.location
        resp = self.client.post("/edit_course/",
                                {"name": self.testCourse.name, "location": "", "hours": self.testCourse.hours,
                                 "days": self.testCourse.days, "instructor": self.testCourse.instructor.userID,
                                 "submit": self.testCourse.courseID})
        self.assertEqual(resp.context["error"], "Course was not edited. Location should not be left blank",
                         "An error message was not displayed when location was left blank")
        self.assertEqual(location, Course.objects.get(courseID=self.testCourse.courseID).location,
                         "Location was changed when it shouldn't have been")

    def test_editHours(self):
        self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                           "hours": "11:00 AM - 12:00 PM", "days": self.testCourse.days,
                                           "instructor": self.testCourse.instructor.userID,
                                           "submit": self.testCourse.courseID})
        self.assertEqual("11:00 AM - 12:00 PM", Course.objects.get(courseID=self.testCourse.courseID).hours,
                         "Course hours were not set correctly")

    def test_editBlankHours(self):
        hours = self.testCourse.hours
        resp = self.client.post("/edit_course/",
                                {"name": self.testCourse.name, "location": self.testCourse.location, "hours": "",
                                 "days": self.testCourse.days, "instructor": self.testCourse.instructor.userID,
                                 "submit": self.testCourse.courseID})
        self.assertEqual(resp.context["error"], "Course was not edited. Hours should not be left blank",
                         "An error message was not displayed when hours were left blank")
        self.assertEqual(hours, Course.objects.get(courseID=self.testCourse.courseID).hours,
                         "Hours were changed when they shouldn't have been")

    def test_editInvalidHours(self):
        hours = self.testCourse.hours
        resp = self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                                  "hours": "invalid input", "days": self.testCourse.days,
                                                  "instructor": self.testCourse.instructor.userID,
                                                  "submit": self.testCourse.courseID})
        self.assertEqual(resp.context["error"],
                         "Course was not edited. Wrong format for hours. Format should be HH:MM AM/PM - HH:MM AM/PM",
                         "An error message was not displayed when hours entered incorrectly")
        self.assertEqual(hours, Course.objects.get(courseID=self.testCourse.courseID).hours,
                         "Hours were changed when they shouldn't have been")

    def test_editDays(self):
        self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                           "hours": self.testCourse.hours, "days": "T, Th",
                                           "instructor": self.testCourse.instructor.userID,
                                           "submit": self.testCourse.courseID})
        self.assertEqual("T, Th", Course.objects.get(courseID=self.testCourse.courseID).days,
                         "Course days were not set correctly")

    def test_editBlankDays(self):
        days = self.testCourse.days
        resp = self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                                  "hours": self.testCourse.hours, "days": "",
                                                  "instructor": self.testCourse.instructor.userID,
                                                  "submit": self.testCourse.courseID})
        self.assertEqual(resp.context["error"], "Course was not edited. At least one day must be selected",
                         "An error message was not displayed when the days were left unpicked")
        self.assertEqual(days, Course.objects.get(courseID=self.testCourse.courseID).days,
                         "Days were changed when they shouldn't have been")

    def test_editInstructor(self):
        self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                           "hours": self.testCourse.hours, "days": self.testCourse.days,
                                           "instructor": self.newInstructor.userID, "submit": self.testCourse.courseID})
        self.assertEqual(self.newInstructor, Course.objects.get(courseID=self.testCourse.courseID).instructor,
                         "Course instructor was not set correctly")

    def test_editTAs(self):
        self.client.post("/edit_course/", {"name": self.testCourse.name, "location": self.testCourse.location,
                                           "hours": self.testCourse.hours, "days": self.testCourse.days,
                                           "instructor": self.instructor.userID, "TAs": [self.TA.userID],
                                           "submit": self.testCourse.courseID})
        self.assertIn(self.TA, Course.objects.get(courseID=self.testCourse.courseID).TAs.all(),
                      "Course TAs were not set correctly")
