from django.test import TestCase, Client
from TAScheduler.models import *


# Delete User Cases: Successful Delete,
# If a user deletes himself sent back to login
# Cannot delete Instructor if assigned to course
# Cannot delete User TA if assigned to lab
class SuccessfulDeleteUser(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None

    def setUp(self):
        self.dummyClient = Client()
        self.TA = UserProfile.objects.create(userID=1, userType="TA", username="TA1", password="TA123", name="TA Dummy",
                                             address="TA Address",
                                             phone=3234457876, email="TAEmail@email.com")

        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Instructor1",
                                                     password="Instructor123", name="Instructor Dummy",
                                                     address="Instructor Address", phone=3234457176,
                                                     email="InstructorEmail@email.com")

        self.admin = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="Admin1", password="Admin123",
                                                name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.admin2 = UserProfile.objects.create(userID=4, userType="SUPERVISOR", username="Admin2",
                                                 password="Admin2123", name="Admin2 Dummy", address="Admin2 Address",
                                                 phone=3234452176, email="Admin2Email@email.com")

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_deleteUser(self):
        self.dummyClient.post('/delete_user/', {'delete': 1}, follow=True)
        var = UserProfile.objects.count()
        self.assertEquals(var, 3, "TA has been successfully deleted")
        allUsers = list(UserProfile.objects.all())
        self.assertEquals(allUsers, [self.instructor, self.admin, self.admin2],
                          "Instructor, Admin, and Admin2 still exist")

        self.dummyClient.post('/delete_user/', {'delete': 2}, follow=True)
        var = UserProfile.objects.count()
        self.assertEquals(var, 2, "Instructor has been successfully deleted")
        allUsers = list(UserProfile.objects.all())
        self.assertEquals(allUsers, [self.admin, self.admin2], "Admin2 and Admin has not been deleted")

        self.dummyClient.post('/delete_user/', {'delete': 4}, follow=True)
        var = UserProfile.objects.count()
        self.assertEquals(var, 1, "Admin2 was successfully deleted")
        allUsers = list(UserProfile.objects.all())
        self.assertEquals(allUsers, [self.admin], "Only admin is left")


class DeleteYourself(TestCase):
    dummyClient = None
    admin = None

    def setUp(self):
        self.dummyClient = Client()

        self.admin = UserProfile.objects.create(userID=1, userType="SUPERVISOR", username="Admin1", password="Admin123",
                                                name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_deleteYourself(self):
        resp = self.dummyClient.post('/delete_user/', {'delete': 1}, follow=True)
        try:
            self.assertTrue(resp.url, "")
        except AttributeError as msg:
            print(msg)


class DeleteInstructorTAsAssignedToCourse(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None
    course = None

    def setUp(self):
        self.dummyClient = Client()
        self.TA = UserProfile.objects.create(userID=1, userType="TA", username="TA1", password="TA123", name="TA Dummy",
                                             address="TA Address",
                                             phone=3234457876, email="TAEmail@email.com")

        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Instructor1",
                                                     password="Instructor123", name="Instructor Dummy",
                                                     address="Instructor Address", phone=3234457176,
                                                     email="InstructorEmail@email.com")

        self.admin = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="Admin1", password="Admin123",
                                                name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.course = Course.objects.create(courseID=1, name="Software Engineering",
                                            location="EMS 180", hours="12:00PM - 01:00PM", days="M, W",
                                            instructor=self.instructor)

        self.course.TAs.add(self.TA)

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_deleteInstructorTAAssignedToCourse(self):
        # self.dummyClient.post('/delete_user/', {'delete': 1}, follow=True)
        # self.assertEquals(UserProfile.objects.get(userID=self.TA.userID), self.TA,
        #                   "TA has not been deleted because it is associated with course")

        self.dummyClient.post('/delete_user/', {'delete': 2}, follow=True)
        self.assertEquals(UserProfile.objects.get(userID=self.instructor.userID), self.instructor,
                          "Instructor has not been deleted because it is associated with Course")


class DeleteTANotAssignedToCourse(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None
    course = None

    def setUp(self):
        self.dummyClient = Client()
        self.TA = UserProfile.objects.create(userID=1, userType="TA", username="TA1", password="TA123", name="TA Dummy",
                                             address="TA Address",
                                             phone=3234457876, email="TAEmail@email.com")

        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Instructor1",
                                                     password="Instructor123", name="Instructor Dummy",
                                                     address="Instructor Address", phone=3234457176,
                                                     email="InstructorEmail@email.com")

        self.admin = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="Admin1", password="Admin123",
                                                name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.course = Course.objects.create(courseID=1, name="Software Engineering",
                                            location="EMS 180", hours="12:00PM - 01:00PM", days="M, W",
                                            instructor=self.instructor)

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_TANotAssignedToCourse(self):
        self.dummyClient.post('/delete_user/', {'delete': 1}, follow=True)
        var = UserProfile.objects.count()
        self.assertEquals(var, 2)
        allUsers = list(UserProfile.objects.all())
        self.assertEquals(allUsers, [self.instructor, self.admin], "TA was successfully deleted")


class DeleteInstructorTAAssignedToLab(TestCase):
    dummyClient = None
    TA = None
    instructor = None
    admin = None
    course = None
    lab = None

    def setUp(self):
        self.dummyClient = Client()
        self.TA = UserProfile.objects.create(userID=1, userType="TA", username="TA1", password="TA123", name="TA Dummy",
                                             address="TA Address",
                                             phone=3234457876, email="TAEmail@email.com")

        self.instructor = UserProfile.objects.create(userID=2, userType="INSTRUCTOR", username="Instructor1",
                                                     password="Instructor123", name="Instructor Dummy",
                                                     address="Instructor Address", phone=3234457176,
                                                     email="InstructorEmail@email.com")

        self.admin = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="Admin1", password="Admin123",
                                                name="Admin Dummy", address="Admin Address",
                                                phone=3234452176, email="AdminEmail@email.com")

        self.course = Course.objects.create(courseID=1, name="Software Engineering",
                                            location="EMS 180", hours="12:00PM - 01:00PM", days="M, W",
                                            instructor=self.instructor)

        self.course.TAs.add(self.TA)

        self.lab = Lab.objects.create(labID=1, name="Lab", location="EMS 280",
                                      hours="03:00PM - 04:00PM", days="M, W", course=self.course, TA=self.TA)

        self.dummyClient.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_deleteTAAssignedToLab(self):
        self.dummyClient.post('/delete_user/', {'delete': 1}, follow=True)
        self.assertEquals(UserProfile.objects.get(userID=self.TA.userID), self.TA,
                          "TA has not been deleted because it is associated with Lab")

        self.dummyClient.post('/delete_user/', {'delete': 2}, follow=True)
        self.assertEquals(UserProfile.objects.get(userID=self.instructor.userID), self.instructor,
                          "Instructor has not been deleted because it is associated with Lab")
