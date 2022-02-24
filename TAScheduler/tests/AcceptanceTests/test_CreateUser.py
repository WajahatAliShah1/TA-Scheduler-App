from django.test import TestCase, Client
from TAScheduler.models import *
from TAScheduler.Management.UserManagement import UserManagement


class TestCreateUser(TestCase):
    def setUp(self):
        self.admin = UserProfile.objects.create(userID=1, userType="SUPERVISOR", username="admin",
                                                password="admin", name="Admin", address="address",
                                                phone=1234567890, email="a@a.com")
        self.client = Client()
        self.client.post("/", {"useraccount": self.admin.username, "password": self.admin.password})

    def test_badID(self):
        r = self.client.post("/create_user/",
                             {"userID": 1, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"],
                         "User was not created. This user already exists: ",
                         "An error message was not displayed when userID was a duplicate")

        self.assertEqual(UserProfile.objects.get(userID=1).userID, 1, "Database was not changed")

    def test_blankUsername(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. Username should not be left blank",
                         "An error message was not displayed when username was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_blankPassword(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. Password should not be left blank",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_blankName(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "", "address": "address",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. Name should not be left blank",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_blankAddress(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. Address should not be left blank",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_blankPhone(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": "",
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_bigPhone(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 123456789123,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. A phone number needs to be 10 digits",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_smallPhone(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 123,
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. A phone number needs to be 10 digits",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_stringPhone(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": "123456789123",
                              "email": "s@s.com"}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. A phone number needs to be 10 digits",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_blankEmail(self):
        r = self.client.post("/create_user/",
                             {"userID": 2, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 1234567891,
                              "email": ""}, follow=True)

        self.assertEqual(r.context["error"], "User was not created. Email should not be left blank",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(UserProfile.objects.count(), 1, "Database did not change")

    def test_createSupervisor(self):
        r = self.client.post("/create_user/",
                             {"userID": 98, "userType": "SUPERVISOR", "username": "supervisorTest",
                              "password": "supervisorTest",
                              "name": "Test Supervisor", "address": "address",
                              "phone": 1234567891,
                              "email": "s@s.com"}, follow=True)

        self.assertNotEqual(UserProfile.objects.get(userID=98),
                            UserProfile(userID=98, userType="SUPERVISOR", username="supervisorTest",
                                        password="supervisorTest", name="Test Supervisor", address="address",
                                        phone=1234567891, email="s@s.com"),
                            "Supervisor was not created successfully")

    def test_createInstructor(self):
        r = self.client.post("/create_user/",
                             {"userID": 99, "userType": "INSTRUCTOR", "username": "InstructorTest",
                              "password": "InstructorTest",
                              "name": "Test Instructor", "address": "address",
                              "phone": 1234567891,
                              "email": "i@i.com"}, follow=True)

        self.assertNotEqual(UserProfile.objects.get(userID=99),
                            UserProfile(userID=99, userType="INSTRUCTOR", username="InstructorTest",
                                        password="InstructorTest", name="Test Instructor", address="address",
                                        phone=1234567891, email="i@i.com"),
                            "Instructor was not created successfully")

    def test_createTA(self):
        r = self.client.post("/create_user/",
                             {"userID": 100, "userType": "TA", "username": "taTest",
                              "password": "taTest",
                              "name": "Test Ta", "address": "address",
                              "phone": 1234567891,
                              "email": "t@t.com"}, follow=True)

        self.assertNotEqual(UserProfile.objects.get(userID=100),
                            UserProfile(userID=100, userType="TA", username="taTest", password="taTest", name="Test Ta",
                                        address="address", phone=1234567891, email="t@t.com"),
                            "TA was not created successfully")
