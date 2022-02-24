from django.test import TestCase, Client

from TAScheduler.models import UserProfile


class TestViewUsersSupervisor(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = UserProfile.objects.create(userID=1, userType="INSTRUCTOR", username="Samuel",
                                                password="Samuel12345", name='Samuel', address="Address1",
                                                phone=9876543212, email="sam@uwm.edu")
        self.user2 = UserProfile.objects.create(userID=2, userType="TA", username="John", password="John12345",
                                                name="John", address="Address2", phone=1234567890, email="john@uwm.edu")
        self.supervisor = UserProfile.objects.create(userID=3, userType="SUPERVISOR", username="supervisor",
                                                     password="password", name="SupervisorGuy",
                                                     address="123 Street Street", phone=3211234567,
                                                     email="supervisor@supervisor.gov")
        self.client.post("/", {"useraccount": self.supervisor.username, "password": self.supervisor.password})
        self.resp = self.client.get("/view_users/")

    def test_userID(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.userID), str(self.resp.content),
                          "User " + user.username + "'s userID did not display")

    def test_userType(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(user.userType, str(self.resp.content),
                          "User " + user.username + "'s userType did not display")

    def test_username(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(user.username, str(self.resp.content),
                          "User " + user.username + "'s username did not display")

    def test_password(self):
        # Should not be displayed
        for user in self.resp.context["user_list"]:
            self.assertNotIn(user.password, str(self.resp.content),
                             "User " + user.username + "'s password displayed when it shouldn't have")

    def test_name(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(user.name, str(self.resp.content),
                          "User " + user.username + "'s name did not display")

    def test_address(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(user.address, str(self.resp.content),
                          "User " + user.username + "'s address did not display")

    def test_phone(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.phone), str(self.resp.content),
                          "User " + user.username + "'s phone number did not display")

    def test_email(self):
        print(self.resp.content)
        for user in self.resp.context["user_list"]:
            self.assertIn(user.email, str(self.resp.content),
                          "User " + user.username + "'s email did not display")


class TestViewUsersInstructor(TestCase):
    def setUp(self):
        TestViewUsersSupervisor.setUp(self)

    def test_userID(self):
        # for user in self.resp.context["user_list"]:
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.userID), str(self.resp.content),
                          "User " + user.username + " 's userID did not display")

    def test_userType(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.userType), str(self.resp.content),
                          "User " + user.username + " 's userType did not display")

    def test_username(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.username), str(self.resp.content),
                          "User " + user.username + " 's username did not display")

    def test_password(self):
        # Should assert false
        for user in self.resp.context["user_list"]:
            if str(self.resp.content).find(user.password) == -1:
                self.assertNotIn(str(user.password), str(self.resp.content),
                                 "User " + user.username + " 's password did not display")

    def test_name(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.name), str(self.resp.content), "User " + user.username + " 's name did not display")

    def test_address(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.address), str(self.resp.content),
                          "User " + user.username + " 's address did not display")

    def test_phone(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.phone), str(self.resp.content),
                          "User " + user.username + " 's phone did not display")

    def test_email(self):
        for user in self.resp.context["user_list"]:
            self.assertIn(str(user.email), str(self.resp.content),
                          "User " + user.username + " 's email did not display")
