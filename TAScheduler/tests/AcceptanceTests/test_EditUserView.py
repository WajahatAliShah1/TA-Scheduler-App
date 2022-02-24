from django.test import TestCase, Client
from TAScheduler.models import *


class test_editUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.userToEdit = UserProfile.objects.create(userID=1, userType="SUPERVISOR", username="supervisor1",
                                                     password="password", name="Ted Supervisor",
                                                     address="345 Street Street", phone=1234567890,
                                                     email="email@email.com")

        self.assignedTA = UserProfile.objects.create(userID=2, userType="TA", username="ta1", password="password",
                                                     name="ta1", address="345 Street Street", phone=6543212345,
                                                     email="email@email.com")
        self.assignedInstructor = UserProfile.objects.create(userID=3, userType="INSTRUCTOR", username="instructor1",
                                                             password="password", name="instructor1",
                                                             address="345 Street Street", phone=9876543234,
                                                             email="email@email.com")
        self.course1 = Course.objects.create(courseID=1, name="course", location="location",
                                             hours="12:00 PM - 01:00 PM",
                                             days="M", instructor=self.assignedInstructor)
        self.course1.TAs.add(self.assignedTA)

    def test_editUserType(self):
        self.client.post("/edit_user/",
                         {"type": "SUPERVISOR", "username": self.userToEdit.username, "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).userType, "SUPERVISOR",
                         "Edit User did not set userType correctly")

    def test_editUsertypeAssignedInstructor(self):
        user_type = self.assignedInstructor.userType
        resp = self.client.post("/edit_user/", {"type": "SUPERVISOR", "username": self.assignedInstructor.username,
                                                "name": self.assignedInstructor.name,
                                                "address": self.assignedInstructor.address,
                                                "phone": self.assignedInstructor.phone,
                                                "email": self.assignedInstructor.email,
                                                "submit": self.assignedInstructor.userID})
        self.assertEqual(resp.context["error"],
                         "User was not changed. An instructor's type cannot be changed while they have courses "
                         "assigned to them",
                         "An error message was not displayed when trying to change type of an instructor with a "
                         "course assigned to them.")
        self.assertEqual(user_type, self.assignedInstructor.userType,
                         "The user's type was changed when it shouldn't have been")

    def test_editUsertypeAssignedTA(self):
        user_type = self.assignedTA.userType
        resp = self.client.post("/edit_user/", {"type": "SUPERVISOR", "username": self.assignedTA.username,
                                                "name": self.assignedTA.name,
                                                "address": self.assignedTA.address,
                                                "phone": self.assignedTA.phone,
                                                "email": self.assignedTA.email,
                                                "submit": self.assignedTA.userID})
        self.assertEqual(resp.context["error"],
                         "User was not changed. An TA's type cannot be changed while they are assigned as a TA of a "
                         "course",
                         "An error message was not displayed when trying to change type of an TA that is assigned to "
                         "a course")
        self.assertEqual(user_type, self.assignedTA.userType, "The user's type was changed when it shouldn't have been")

    def test_editUsername(self):
        self.client.post("/edit_user/",
                         {"type": self.userToEdit.userType, "username": "new username", "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).username, "new username",
                         "Edit user did not set username correctly")

    def test_editBlankUsername(self):
        username = self.userToEdit.username
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": "", "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. Username should not be left blank",
                         "An error message was not displayed when username was left blank")
        self.assertNotEqual(username, self.userToEdit, "The user's username was changed when it shouldn't have been")

    def test_editName(self):
        self.client.post("/edit_user/",
                         {"type": self.userToEdit.userType, "username": self.userToEdit.username, "name": "new name",
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).name, "new name",
                         "Edit User did not set name correctly")

    def test_editBlankName(self):
        name = self.userToEdit.name
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": self.userToEdit.username, "name": "",
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. Name should not be left blank",
                         "An error message was not displayed when name was left blank")
        self.assertEqual(name, self.userToEdit.name, "The user's name was edited when it shouldn't have been")

    def test_editAddress(self):
        self.client.post("/edit_user/",
                         {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                          "name": self.userToEdit.name,
                          "address": "new address", "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).address, "new address",
                         "Edit User did not set address correctly")

    def test_editBlankAddress(self):
        address = self.userToEdit.address
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                                 "name": self.userToEdit.name,
                                 "address": "", "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. Address should not be left blank",
                         "An error message was not displayed when address was left blank")
        self.assertEqual(address, self.userToEdit.address, "The user's address was changed when it shouldn't have been")

    def test_editPhone(self):
        self.client.post("/edit_user/",
                         {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                          "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": 9876543212,
                          "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).phone, 9876543212,
                         "Edit User did not set phone correctly")

    def test_editBlankPhone(self):
        phone = self.userToEdit.phone
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                                 "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": "",
                                 "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when phone was left blank")
        self.assertEqual(phone, self.userToEdit.phone,
                         "The user's phone number was changed when it shouldn't have been")

    def test_editInvalidPhone(self):
        phone = self.userToEdit.phone
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                                 "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": 0,
                                 "email": self.userToEdit.email, "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. A phone number needs to be 10 digits",
                         "An error message was not displayed when an invalid phone number was posted")
        self.assertEqual(phone, self.userToEdit.phone,
                         "The user's phone number was changed when it shouldn't have been")

    def test_editEmail(self):
        self.client.post("/edit_user/",
                         {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                          "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": "newemail@newemail.com", "submit": self.userToEdit.userID})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).email, "newemail@newemail.com",
                         "Edit User did not set email correctly")

    def test_editBlankEmail(self):
        email = self.userToEdit.email
        resp = self.client.post("/edit_user/",
                                {"type": self.userToEdit.userType, "username": self.userToEdit.username,
                                 "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": "", "submit": self.userToEdit.userID})
        self.assertEqual(resp.context["error"], "User was not changed. Email should not be left blank",
                         "An error message was not displayed when email was left blank")
        self.assertEqual(email, self.userToEdit.email)
