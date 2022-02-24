from TAScheduler.models import UserProfile


class UserManagement(object):

    # Preconditions: The user has to have been instantiated.
    #                 The user must be of type administrator
    # Postconditions: Creates a user
    # Side-effects: User is created and added into the database
    # UserId(in) - Id of the user
    # User UserName(in) -  User name of the user
    # User Name(in) - Name of the user
    # User PhoneNumber(in) - Phone Number of the user
    # User Address(in) - Address of the user
    # User Password(in) - Password of the user
    # User Type(in) - Type of the user
    # User Email(in) - Email of the user
    @staticmethod
    def createUser(user_id, user_type, username, password, name, address, phone, email):
        if user_id is None or user_type is None or username is None or password is None or name is None or address is None or phone is None or email is None:
            raise ValueError("Every input is required")
        UserManagement.__inputErrorCheck(user_id, user_type, username, password, name, address, phone, email)

        try:
            UserManagement.findUser(user_id)
        except TypeError:
            UserProfile.objects.create(
                userID=user_id,
                userType=user_type,
                username=username,
                password=password,
                name=name,
                address=address,
                phone=phone,
                email=email
            )
            return
        raise TypeError("This user already exists: ")

    # Preconditions: The user has to have been instantiated.
    #                The user must be of type administrator
    # Postconditions: Edits a user
    # Side-effects: User is edited inside the database
    # UserId(in) - Id of the user
    # User  UserName(in) -  User name of the user
    # User Name(in) - Name of the user
    # User PhoneNumber(in) - Phone Number of the user
    # User Address(in) - Address of the user
    # User Password(in) - Password of the user
    # User Type(in) - Type of the user
    # User Email(in) - Email of the user
    @staticmethod
    def editUser(user_id=None, user_type=None, username=None, password=None, name=None, address=None, phone=None,
                 email=None):
        UserManagement.__inputErrorCheck(user_id, user_type, username, password, name, address, phone, email)

        try:
            change_user = UserManagement.findUser(user_id)
        except TypeError:
            raise TypeError("This user does not exist (editUser): ")
        if not (user_type is None):
            if not (user_type == change_user.userType):
                if change_user.userType == "INSTRUCTOR" and len(change_user.course_set.all()) > 0:
                    raise ValueError("An instructor's type cannot be changed while they have courses assigned to them")
                if change_user.userType == "TA" and len(change_user.TAToCourse.all()) > 0:
                    raise ValueError(
                        "An TA's type cannot be changed while they are assigned as a TA of a course")
                if change_user.userType == "TA" and len(change_user.TAToLab.all()):
                    raise ValueError(
                        "An TA's type cannot be changed while they have lab sections assigned to them")
            change_user.userType = user_type
        if not (username is None):
            change_user.username = username
        if not (password is None):
            change_user.password = password
        if not (name is None):
            change_user.name = name
        if not (address is None):
            change_user.address = address
        if not (phone is None):
            change_user.phone = phone
        if not (email is None):
            change_user.email = email
        change_user.save()

    # Preconditions: The user has to have been instantiated
    #   There are accounts to display
    # Postconditions: Displays the user
    # Side-effects: None
    # UserId(in) - Id of the user
    # UserProfile(out) - Returns the user found
    @staticmethod
    def findUser(user_id=None, username=None):
        if not (user_id is None):
            UserManagement.__inputErrorCheck(user_id=user_id, username=username)
            try:
                profile = UserProfile.objects.get(userID=user_id)
            except UserProfile.DoesNotExist:
                profile = None

            if profile is None:
                raise TypeError("This ID does not exist")
        elif not (username is None):
            try:
                profile = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                profile = None

            if profile is None:
                raise TypeError("This username does not exist")
        else:
            raise TypeError("Unknown error")
        return profile

    # Preconditions: The user has to have been instantiated
    # The user must be of type administrator
    # Postconditions: User is deleted
    # Side-effects: User is deleted so it is removed from the database
    # UserId(in) - Id of the user
    @staticmethod
    def deleteUser(user_id):
        UserManagement.findUser(user_id=user_id).delete()

    @staticmethod
    def __inputErrorCheck(user_id=None, user_type=None, username=None, password=None, name=None, address=None,
                          phone=None, email=None):
        if not (user_id is None):
            if not (isinstance(user_id, int)):
                raise TypeError("Id entered is not of type int")
        if not (user_type is None):
            if not (isinstance(user_type, str)):
                raise TypeError("userType entered is not of type str")
            if not (user_type in ["SUPERVISOR", "INSTRUCTOR", "TA"]):
                raise ValueError("userType entered is not a valid userType")
        if not (username is None):
            if not (isinstance(username, str)):
                raise TypeError("Username entered is not of type str")
            if not (len(username)) > 0:
                raise ValueError("Username should not be left blank")
        if not (password is None):
            if not (isinstance(password, str)):
                raise TypeError("Password entered is not of type str")
            if not (len(password)) > 0:
                raise ValueError("Password should not be left blank")
        if not (name is None):
            if not (isinstance(name, str)):
                raise TypeError("Name entered is not of type str")
            if not (len(name)) > 0:
                raise ValueError("Name should not be left blank")
        if not (address is None):
            if not (isinstance(address, str)):
                raise TypeError("Address entered is not of type str")
            if not (len(address)) > 0:
                raise ValueError("Address should not be left blank")
        if not (phone is None):
            if not (isinstance(int(phone), int)):
                raise TypeError("Contact entered is not of type str")
            if not (1000000000 < phone < 9999999999):
                raise ValueError("A phone number needs to be 10 digits")
        if not (email is None):
            if not (isinstance(email, str)):
                raise TypeError("Email entered is not of type str")
            if not (len(email)) > 0:
                raise ValueError("Email should not be left blank")
