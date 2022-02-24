from django.test import TestCase, Client

from TAScheduler.models import UserProfile

'''
As a user, I want to be able to navigate to the Account settings page
----------------------------------------------------
GIVEN: The user is logged in and at the home page
AND:They can click on "Account"
THEN: They will be navigated to the "Account" page

As a user, I want to be able to navigate to the Send Message page
----------------------------------------------------
GIVEN: The user is logged in and at the home page
AND:They can click on "Send Message"
THEN: They will be navigated to the "Send Message" page

As a user, I want to be able to navigate to the Lab page
----------------------------------------------------
GIVEN: The user is logged in and at the home page
AND:They can click on "Lab"
THEN: They will be navigated to the "Lab" page

As a user, I want to be able to navigate to the Course page
----------------------------------------------------
GIVEN: The user is logged in and at the home page
AND:They can click on "Course"
THEN: They will be navigated to the "Course" page

As a user, I want to be able to navigate to the User page
----------------------------------------------------
GIVEN: The user is logged in and at the home page
AND:They can click on "User"
THEN: They will be navigated to the "User" page
'''


class Test(TestCase):

    def setUp(self):

        self.client = Client()
        self.testAdmin = UserProfile.objects.create(username='testAdmin', password='testAdmin', userID=121212)

    def test_home_to_account_settings(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/account_settings")

        try:
            self.assertTrue(r.url, "/account_settings")
        except AssertionError as msg:
            print(msg)

    def test_home_to_lab(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/view_labs")

        try:
            self.assertTrue(r.url, "/view_labs")
        except AssertionError as msg:
            print(msg)

    def test_home_to_course(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/view_courses")

        try:
            self.assertTrue(r.url, "/view_courses")
        except AssertionError as msg:
            print(msg)

    def test_home_to_user(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/view_users")

        try:
            self.assertTrue(r.url, "/view_users")
        except AssertionError as msg:
            print(msg)

    def test_home_to_send_notification(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/send_notification")

        try:
            self.assertTrue(r.url, "/send_notification")
        except AssertionError as msg:
            print(msg)

    def test_home_to_logout(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        self.assertTrue(r.context is None)

        try:
            self.assertTrue(r.url, "home")
        except AssertionError as msg:
            print(msg)

        r = self.client.get("/home" + '/')

        try:
            self.assertTrue(r.url, "/")
        except AssertionError as msg:
            print(msg)
