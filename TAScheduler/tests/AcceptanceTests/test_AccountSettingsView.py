from django.test import TestCase, Client
from TAScheduler.models import *


class test_editUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.userToEdit = UserProfile.objects.create(userID=1, userType="SUPERVISOR", username="supervisor1",
                                                     password="password", name="Ted Supervisor",
                                                     address="345 Street Street", phone=1234567890,
                                                     email="email@email.com")
        self.client.post("/", {"useraccount": self.userToEdit.username, "password": self.userToEdit.password})

    def test_editUsername(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": "new username",
                          "password": self.userToEdit.password, "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).username, "new username",
                         "Account Settings did not set username correctly")

    def test_editBlankUsername(self):
        username = self.userToEdit.username
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": "",
                                 "password": self.userToEdit.password, "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. Username should not be left blank",
                         "An error message was not displayed when username was left blank")
        self.assertNotEqual(username, self.userToEdit, "The user's username was changed when it shouldn't have been")

    def test_editPassword(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                          "password": "newpassword", "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).password, "newpassword",
                         "Account Settings did not set password correctly")

    def test_editBlankPassword(self):
        password = self.userToEdit.password
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username, "password": "",
                                 "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. Password should not be left blank",
                         "An error message was not displayed when password was left blank")
        self.assertEqual(password, self.userToEdit.password,
                         "The user's password was edited when it shouldn't have been")

    def test_editName(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                          "password": self.userToEdit.password, "name": "new name",
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).name, "new name",
                         "Account Settings did not set name correctly")

    def test_editBlankName(self):
        name = self.userToEdit.name
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                                 "password": self.userToEdit.password, "name": "",
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. Name should not be left blank",
                         "An error message was not displayed when name was left blank")
        self.assertEqual(name, self.userToEdit.name, "The user's name was edited when it shouldn't have been")

    def test_editAddress(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                          "password": self.userToEdit.password, "name": self.userToEdit.name,
                          "address": "new address", "phone": self.userToEdit.phone,
                          "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).address, "new address",
                         "Account Settings did not set address correctly")

    def test_editBlankAddress(self):
        address = self.userToEdit.address
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                                 "password": self.userToEdit.password, "name": self.userToEdit.name,
                                 "address": "", "phone": self.userToEdit.phone,
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. Address should not be left blank",
                         "An error message was not displayed when address was left blank")
        self.assertEqual(address, self.userToEdit.address, "The user's address was changed when it shouldn't have been")

    def test_editPhone(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                          "password": self.userToEdit.password, "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": 9876543212,
                          "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).phone, 9876543212,
                         "Account Settings did not set phone correctly")

    def test_editBlankPhone(self):
        phone = self.userToEdit.phone
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                                 "password": self.userToEdit.password, "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": "",
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. invalid literal for int() with base 10: ''",
                         "An error message was not displayed when phone was left blank")
        self.assertEqual(phone, self.userToEdit.phone,
                         "The user's phone number was changed when it shouldn't have been")

    def test_editInvalidPhone(self):
        phone = self.userToEdit.phone
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                                 "password": self.userToEdit.password, "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": 45,
                                 "email": self.userToEdit.email, "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. A phone number needs to be 10 digits",
                         "An error message was not displayed when an invalid phone number was posted")
        self.assertEqual(phone, self.userToEdit.phone,
                         "The user's phone number was changed when it shouldn't have been")

    def test_editEmail(self):
        self.client.post("/account_settings/",
                         {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                          "password": self.userToEdit.password, "name": self.userToEdit.name,
                          "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                          "email": "newemail@newemail.com", "edit": ""})
        self.assertEqual(UserProfile.objects.get(userID=self.userToEdit.userID).email, "newemail@newemail.com",
                         "Account Settings did not set email correctly")

    def test_editBlankEmail(self):
        email = self.userToEdit.email
        resp = self.client.post("/account_settings/",
                                {"userID": self.userToEdit.userID, "username": self.userToEdit.username,
                                 "password": self.userToEdit.password, "name": self.userToEdit.name,
                                 "address": self.userToEdit.address, "phone": self.userToEdit.phone,
                                 "email": "", "edit": ""})
        self.assertEqual(resp.context["error"], "User was not changed. Email should not be left blank",
                         "An error message was not displayed when email was left blank")
        self.assertEqual(email, self.userToEdit.email)
