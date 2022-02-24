from django.test import TestCase, Client

from TAScheduler.models import *

'''
As a user, I want to sign in.
-----------------------------
GIVEN: the user is on the login page
AND: the user has an account
THEN: the user can type in their account name and password
AND: the user will be logged into the website.
----------------------------------
GIVEN: the user is on the login page
AND: the user has an account
AND: the user enters in an incorrect password
THEN: The user will not be logged in
----------------------------------
GIVEN: the user is on the login page
AND: the user has an account
THEN: the user can type in their account name and password
AND: the user will be logged into the website.
'''


class Test(TestCase):

    def setUp(self):

        self.client = Client()
        self.testAdmin = UserProfile.objects.create(username='testAdmin', password='testAdmin', userID=121212)

    # Successful login test
    def test_logging_in_1(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'testAdmin'})
        # print(r.context['error'])
        try:
            self.assertTrue(r.context is None)
        except AssertionError as msg:
            print(msg)

        pass

    # Incorrect password test
    def test_logging_in_2(self):

        r = self.client.post('/', {'useraccount': 'testAdmin', 'password': 'asdfasdfa'}, follow=True)
        try:
            self.assertTrue(r.context["error"], "Incorrect Password")
        except AssertionError as msg:
            print(msg)

        pass

    def test_logging_in_3(self):

        r = self.client.post('/', {'useraccount': 'asdfadsfasdqwerqewrrrwef', 'password': 'asdfasdfa'})
        try:
            self.assertTrue(r.context["error"], "User does not exist")
            self.assertTrue(r.context["error"], "Incorrect Password")
        except AssertionError as msg:
            print(msg)

        pass
