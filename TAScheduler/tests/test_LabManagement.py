from django.test import TestCase
from TAScheduler.Management.LabManagement import LabManagement
from TAScheduler.models import *


class CreateLabTests(TestCase):
    def setUp(self):
        UserProfile.objects.create(userID=1, userType="TA", username="Apoorv", password="password",
                                   name="Apoorv Prasad", address="Address", phone=7176547245, email="apoorv@uwm.edu")
        self.TA = UserProfile.objects.get(userID=1)
        UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Rock", password="password",
                                   name="Jason Rock", address="Address", phone=8765436785, email="rock@uwm.edu")
        self.instructor = UserProfile.objects.get(userID=2)
        Course.objects.create(courseID=10, name="Software Engineering", location="EMS180", hours="10:00 AM - 10:50 AM",
                              days="M, W", instructor=self.instructor)
        self.course = Course.objects.get(courseID=10)
        self.course.TAs.add(self.TA)
        LabManagement.createLab(lab_id=100, lab_name="Software Engineering Lab", lab_location="EMS180",
                                lab_hours="10:00 AM - 10:50 AM", lab_days="M, W", course=self.course, ta=self.TA)
        self.testLab = Lab.objects.get(labID=100)

    def test_labID(self):
        self.assertEqual(100, self.testLab.labID, "Lab id was not set correctly when creating lab")

    def test_labIDInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed an user_id with invalid type"):
            LabManagement.createLab(lab_id="String", lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days="M, W", course=self.course, ta=self.TA)

    def test_labIDPreexisting(self):
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createCourse was passed a courseID that already "
                                   "exists in the database"):
            LabManagement.createLab(lab_id=100, lab_name="Computer Programming Lab", lab_location="EMS E240",
                                    lab_days="M, W, F", lab_hours="12:00 PM - 12:50 PM", course=self.course, ta=self.TA)

    def test_labName(self):
        self.assertEqual("Software Engineering Lab", self.testLab.name,
                         "Lab name was not set correctly when creating lab")

    def test_labNameInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed a name with invalid type"):
            LabManagement.createLab(lab_id=101, lab_name=93485, lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days="M, W", course=self.course, ta=self.TA)

    def test_labLocation(self):
        self.assertEqual("EMS180", self.testLab.location, "Lab location was not set correctly when creating lab")

    def test_labLocationInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed a location with invalid type"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location=93745,
                                    lab_hours="10:00 AM - 10:50 AM", lab_days="M, W", course=self.course, ta=self.TA)

    def test_labHours(self):
        self.assertEqual("10:00 AM - 10:50 AM", self.testLab.hours, "Lab hours was not set correctly when creating lab")

    def test_labHoursInvalid(self):
        with self.assertRaises(ValueError, msg="An error was not raised when createLab was passed invalid hours"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="invalid", lab_days="M, W", course=self.course, ta=self.TA)

    def test_labHoursInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed hours of an invalid type"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours=12, lab_days="M, W", course=self.course, ta=self.TA)

    def test_labDays(self):
        self.assertEqual("M, W", self.testLab.days, "Lab days were not set correctly when creating lab")

    def test_labDaysInvalid(self):
        with self.assertRaises(ValueError, msg="An error was not raised when createLab was passed invalid days"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days="Invalid", course=self.course, ta=self.TA)

    def test_labDaysInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed hours of an invalid type"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days=126, course=self.course, ta=self.TA)

    def test_labCourse(self):
        self.assertEqual(self.course, self.testLab.course, "Lab course was not set correctly when lab was created")

    def test_labCourseInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed a course of an invalid type"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days=126, course=123, ta=self.TA)

    def test_labTA(self):
        self.assertEqual(self.TA, self.testLab.TA, "Lab TA was not set correctly when lab was created")

    def test_labTAInvalidType(self):
        with self.assertRaises(TypeError,
                               msg="An error was not raised when createLab was passed a course of an invalid type"):
            LabManagement.createLab(lab_id=101, lab_name="Software Engineering Lab", lab_location="EMS180",
                                    lab_hours="10:00 AM - 10:50 AM", lab_days=126, course=self.course, ta=1234)


class EditLabTests(TestCase):
    def setUp(self):
        UserProfile.objects.create(userID=1, userType="TA", username="Apoorv", password="password",
                                   name="Apoorv Prasad", address="Address", phone=7176547245, email="apoorv@uwm.edu")
        UserProfile.objects.create(userID=2, userType="TA", username="username", password="password", name="name",
                                   address="address", phone=7865643678, email="blank@blank.com")
        self.TA1 = UserProfile.objects.get(userID=1)
        self.TA2 = UserProfile.objects.get(userID=2)

        UserProfile.objects.create(userID=3, userType="INSTRUCTOR", username="Rock", password="password",
                                   name="Jason Rock", address="Address", phone=8765436785, email="rock@uwm.edu")
        self.instructor = UserProfile.objects.get(userID=3)
        Course.objects.create(courseID=10, name="Software Engineering", location="EMS180", hours="10:00 AM - 10:50 AM",
                              days="M, W", instructor=self.instructor)
        Course.objects.create(courseID=11, name="System Programming", location="EMS180", hours="10:00 AM - 10:50 AM",
                              days="T, Th", instructor=self.instructor)
        self.course1 = Course.objects.get(courseID=10)
        self.course2 = Course.objects.get(courseID=11)
        self.course1.TAs.add(self.TA1)
        self.course2.TAs.add(self.TA2)
        Lab.objects.create(labID=100, name="Software Engineering Lab", location="EMS180", hours="10:00 AM - 10:50 AM",
                           days="M, W", course=self.course1, TA=self.TA1)
        self.testLab = Lab.objects.get(labID=100)

    def test_invalidID(self):
        with self.assertRaises(TypeError,
                               msg="editLab does not raise an error when passed a labID that doesn't correspond to a "
                                   "lab"):
            LabManagement.editLab(lab_id=787, lab_name="Chemistry lab", lab_location="Location",
                                  lab_hours="12:00 PM - 12:50 PM", lab_days="M, W, F", course=self.course1, ta=self.TA1)

    def test_editName(self):
        LabManagement.editLab(lab_id=self.testLab.labID, lab_name="Changed Name")
        self.assertEqual("Changed Name", Lab.objects.get(labID=100).name, "Name was not edited correctly.")

    def test_editLocation(self):
        LabManagement.editLab(lab_id=self.testLab.labID, lab_location="Physics 120")
        self.assertEqual("Physics 120", Lab.objects.get(labID=100).location, "Location was not edited correctly.")

    def test_editHours(self):
        LabManagement.editLab(lab_id=self.testLab.labID, lab_hours="07:00 PM - 08:00 PM")
        self.assertEqual("07:00 PM - 08:00 PM", Lab.objects.get(labID=100).hours, "Hours were not edited correctly.")

    def test_editDays(self):
        LabManagement.editLab(lab_id=self.testLab.labID, lab_days="T, Th")
        self.assertEqual("T, Th", Lab.objects.get(labID=100).days, "Days were not edited correctly.")

    def test_editCourse(self):
        LabManagement.editLab(lab_id=self.testLab.labID, course=self.course2)
        self.assertEqual(self.course2, Lab.objects.get(labID=100).course, "Course was not edited correctly")

    def test_editTA(self):
        self.course1.TAs.add(self.TA2)
        self.course1.save()
        LabManagement.editLab(lab_id=self.testLab.labID, ta=self.TA2)
        self.assertEqual(self.TA2, Lab.objects.get(labID=100).TA, "TA was not edited correctly.")


class DeleteLabTests(TestCase):
    def setUp(self):
        UserProfile.objects.create(userID=1, userType="TA", username="Apoorv", password="password",
                                   name="Apoorv Prasad", address="Address", phone=7176547245, email="apoorv@uwm.edu")
        self.TA = UserProfile.objects.get(userID=1)
        UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Rock", password="password",
                                   name="Jason Rock", address="Address", phone=8765436785, email="rock@uwm.edu")
        self.instructor = UserProfile.objects.get(userID=2)
        Course.objects.create(courseID=10, name="Software Engineering", location="EMS180", hours="10:00 AM - 10:50 AM",
                              days="M, W", instructor=self.instructor)
        self.course = Course.objects.get(courseID=10)
        Lab.objects.create(labID=100, name="Software Engineering Lab", location="EMS180", hours="10:00 AM - 10:50 AM",
                           days="M, W", course=self.course, TA=self.TA)
        self.testLab = Lab.objects.get(labID=100)

    def test_delete(self):
        LabManagement.deleteLab(lab_id=100)
        self.assertFalse(Lab.objects.filter(labID=100).exists())

    def test_deleteInvalid(self):
        with self.assertRaises(ValueError, msg="An exception was not raised when delete was passed a lab_id that "
                                               "does not exist"):
            LabManagement.deleteLab(lab_id=11)

    def test_deleteCascade(self):
        Course.objects.get(courseID=self.course.courseID).delete()
        self.assertFalse(Lab.objects.filter(labID=100).exists())
