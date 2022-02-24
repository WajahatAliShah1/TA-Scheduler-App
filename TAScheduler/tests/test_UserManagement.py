from django.test import TestCase
from TAScheduler.Management.UserManagement import UserManagement
from TAScheduler.models import *


class TestMyUser(TestCase):

    def setUp(self):
        """
        testusr0: to be empty at all times.
        testusr1: has every field filled off the bat.
        #ID, name, contact, ssn, address, password, userType (we'll use numerical flags for this)
        testusr2: to be used for all of the "set" functions.
        """

        UserManagement.createUser(user_id=1000, user_type="SUPERVISOR", username="mrwick123",
                                  password="password",
                                  name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
                                  phone=4142542688,
                                  email="johnwick123@uwm.edu")
        UserManagement.createUser(user_id=1001, user_type="INSTRUCTOR", username="mrbond123",
                                  password="password",
                                  name="James Bond", address="123 Kenwood Ave, Milwaukee, Wisconsin 99999",
                                  phone=4144567890,
                                  email="jamesbond123@uwm.edu")

        self.testUser = UserProfile.objects.get(userID=1000, userType="SUPERVISOR", username="mrwick123",
                                                password="password",
                                                name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
                                                phone=4142542688,
                                                email="johnwick123@uwm.edu")

        # Course.objects.create(courseID=1001, name="System Programming", location="EMS 180", days="T, Th",
        #                       hours="10:00 AM - 10:50 AM", instructor=self.instructor)
        # self.testCourse = Course.objects.get(courseID=1000)
        # self.testCourse = Course.objects.get(courseID=1000)

    def test_UserID(self):
        self.assertEqual(1000, self.testUser.userID, "User ID was not set correctly when creating a User.")

    def test_InvalidUserID(self):
        # self.assertEqual(1000, self.testUser.UserID, "User ID was not set correctly when creating a User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a courseID with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type="SUPERVISOR", username="johndoe", password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserType(self):
        self.assertEqual("SUPERVISOR", self.testUser.userType, "User type was not set correctly when creating a User.")

    def test_InvalidUserType(self):
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a user type with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type=123, username="johndoe", password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserUsername(self):
        self.assertEqual("mrwick123", self.testUser.username, "User username was not set correctly when "
                                                              "creating a User.")

    def test_InvalidUsername(self):
        # self.assertEqual("not johnwick", self.testUser.UserUsername, "User username was not set correctly when "
        #                                                              "creating a User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a Username with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type="SUPERVISOR", username=123, password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserPassword(self):
        self.assertEqual("password", self.testUser.password, "User Password was not set correctly when creating a "
                                                             "User.")

    def test_InvalidUserPassword(self):
        # self.assertEqual("incorrectPassword", self.testUser.UserPassword, "User Password was not set correctly when "
        #                                                                   "creating a User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a password with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type="SUPERVISOR", username="johndoe", password=5432345,
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserName(self):
        self.assertEqual("John Wick", self.testUser.name, "User Name was not set correctly when creating a User.")

    def test_InvalidUserName(self):
        # self.assertEqual("notmrwick123", self.testUser.UserName, "User Name was not set correctly when creating a
        # User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a Name with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type=123, username="johndoe", password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserAddress(self):
        self.assertEqual("894 Lake Street, Milwaukee, Wisconsin 99999", self.testUser.address, "User Address was "
                                                                                               "not set correctly"
                                                                                               " when creating a "
                                                                                               "User.")

    def test_InvalidUserAddress(self):
        # self.assertEqual("123 Kenwood Ave, Milwaukee, Wisconsin 53211", self.testUser.UserAddress, "User Address was "
        #                                                                                            "not set correctly"
        #                                                                                            " when creating a "
        #                                                                                            "User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed an address with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type=123, username="johndoe", password="john123",
                                      name="John Doe",
                                      address=123, phone=4142340987, email="johndoe123@uwm.edu")

    def test_UserPhone(self):
        self.assertEqual(4142542688, self.testUser.phone, "User Phone was not set correctly when creating a User.")

    def test_InvalidUserPhone(self):
        # self.assertEqual(4141245944, self.testUser.UserPhone, "User Phone was not set correctly when creating a
        # User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a phone number with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type=123, username="johndoe", password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone="4142340987", email="johndoe123@uwm.edu")

    def test_UserEmail(self):
        self.assertEqual("johnwick123@uwm.edu", self.testUser.email, "User Email was not set correctly when "
                                                                     "creating a User.")

    def test_InvalidUserEmail(self):
        # self.assertEqual("notjohnwick123@uwm.edu", self.testUser.UserEmail, "User Email was not set correctly when "
        #                                                                     "creating a User.")
        with self.assertRaises(TypeError,
                               msg="An exception was not raised when createUser was passed a courseID with an "
                                   "invalid type"):
            UserManagement.createUser(user_id=1001, user_type=123, username="johndoe", password="john123",
                                      name="John Doe",
                                      address="3400 N Maryland Ave, Milwaukee, Wisconsin 53211",
                                      phone=4142340987, email=123456)

    def test_EditUser(self):
        UserManagement.editUser(user_id=1000)
        self.assertTrue(UserProfile.objects.filter(userID=1000).exists())

    def test_deleteUser(self):
        UserManagement.deleteUser(user_id=1000)
        self.assertFalse(UserProfile.objects.filter(userID=1000).exists())


class TestEditUser(TestCase):
    def setUp(self):
        UserManagement.createUser(user_id=1000, user_type="SUPERVISOR", username="mrwick123",
                                  password="password",
                                  name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
                                  phone=4142542688,
                                  email="johnwick123@uwm.edu")
        self.supervisor = UserProfile.objects.get(userID=1000)
        UserManagement.createUser(user_id=1001, user_type="INSTRUCTOR", username="mrbond123",
                                  password="password",
                                  name="James Bond", address="123 Kenwood Ave, Milwaukee, Wisconsin 99999",
                                  phone=4144567890,
                                  email="jamesbond123@uwm.edu")
        self.instructor = UserProfile.objects.get(userID=1001)
        UserManagement.createUser(user_id=1002, user_type="TA", username="willferrell123",
                                  password="password",
                                  name="Will Ferrell",
                                  address="123 Hollywood Blvd, Madison, Wisconsin 53207",
                                  phone=4140394122,
                                  email="willferrell123@uwm.edu")
        self.TA = UserProfile.objects.get(userID=1002)
        self.testUser = UserProfile.objects.get(userID=1000, userType="SUPERVISOR", username="mrwick123",
                                                password="password",
                                                name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
                                                phone=4142542688,
                                                email="johnwick123@uwm.edu")

    def test_editUserID(self):
        UserManagement.editUser(user_id=1002)
        self.assertEqual(1002, UserProfile.objects.get(userID=1002).userID, "UserID was not edited correctly.")

    # def test_invalidID(self):
    #     with self.assertRaises(TypeError,
    #                            msg="editUser does not raise an error when passed a userID that doesn't correspond "
    #                                "to a user"):
    #         UserManagement.editUser(userID=1000, userType="SUPERVISOR", username="mrwick123",
    #                                 password="password",
    #                                 name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
    #                                 phone=4142542688,
    #                                 email="johnwick123@uwm.edu")

    def test_editUserType(self):
        UserManagement.editUser(user_id=1002, user_type="TA")
        self.assertEqual("TA", UserProfile.objects.get(userID=1002).userType, "User Type was not edited correctly.")

    # def test_editInvalidUserType(self):
    #     with self.assertRaises(TypeError,
    #                            msg="editUser does not raise an error when passed a userID that doesn't correspond "
    #                                "to a user"):
    #         UserManagement.editUser(userID=1000, userType="SUPERVISOR", username="mrwick123",
    #                                 password="password",
    #                                 name="John Wick", address="894 Lake Street, Milwaukee, Wisconsin 99999",
    #                                 phone=4142542688,
    #                                 email="johnwick123@uwm.edu")

    def test_editUsername(self):
        UserManagement.editUser(user_id=1002, username="willferrell123")
        self.assertEqual("willferrell123", UserProfile.objects.get(userID=1002).username,
                         "Username was not edited correctly.")

    def test_editPassword(self):
        UserManagement.editUser(user_id=1002, password="password")
        self.assertEqual("password", UserProfile.objects.get(userID=1002).password,
                         "Password was not edited correctly.")

    def test_editName(self):
        UserManagement.editUser(user_id=1002, name="John Wick")
        self.assertEqual("John Wick", UserProfile.objects.get(userID=1002).name, "Name was not edited correctly.")

    def test_editAddress(self):
        UserManagement.editUser(user_id=1000, address="894 Lake Street, Milwaukee, Wisconsin 99999")
        self.assertEqual("894 Lake Street, Milwaukee, Wisconsin 99999", UserProfile.objects.get(userID=1000).address,
                         "Location was not edited correctly.")

    def test_editPhone(self):
        UserManagement.editUser(user_id=1002, phone=4140394122)
        self.assertEqual(4140394122, UserProfile.objects.get(userID=1002).phone,
                         "Phone was not edited correctly.")

    def test_editEmail(self):
        UserManagement.editUser(user_id=1002, email="willferrell123@uwm.edu")
        self.assertEqual("willferrell123@uwm.edu", UserProfile.objects.get(userID=1002).email,
                         "Email was not edited correctly.")


class TestDeleteUser(TestCase):
    def setUp(self):
        UserManagement.createUser(user_id=1, user_type="INSTRUCTOR", username="instructor", password="password",
                                  name="Professor Layton", address="3400 N Maryland Ave", phone=6085555432,
                                  email="layton@gmail.com")
        self.instructor = UserProfile.objects.get(userID=1)
        UserProfile.objects.create(userID=10, userType="SUPERVISOR", username="WillFerrell", password="comedy",
                                   name="Will Ferrell", address="3400 N Maryland Ave", phone="6085555432",
                                   email="layton@gmail.com")

    def test_delete(self):
        UserManagement.deleteUser(user_id=1)
        self.assertFalse(UserProfile.objects.filter(userID=1).exists())
