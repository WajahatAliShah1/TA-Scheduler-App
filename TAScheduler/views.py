from django.shortcuts import render, redirect
from django.views import View
from .models import *
from TAScheduler.Management.UserManagement import UserManagement
from TAScheduler.Management.CourseManagement import CourseManagement
from TAScheduler.Management.LabManagement import LabManagement
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import ProtectedError


# Create your views here.
# A method to check if a user is allowed to view a certain webpage based on their userType. Included a check for if
# the user is not logged in
# request: The request of the current user. From this we can get the user's name using request.session["name"]
# valid_types: A list of all the types allowed to access the page. Should be all caps.
def userAllowed(request, valid_types):
    isValid = True
    if not (request.session["user_type"] in valid_types):
        isValid = False
    return isValid


class Login(View):
    @staticmethod
    def get(request):
        request.session["username"] = None
        request.session["user_type"] = None
        request.session["user_id"] = None
        return render(request, "login.html")

    @staticmethod
    def post(request):
        noUser = False
        incorrectPassword = False
        checkUser = UserProfile
        try:
            # checks to see if a user with the given name exists
            checkUser = UserManagement.findUser(username=request.POST["useraccount"])
            # if the name does exist, checks if the password is correct and sets incorrectPassword accordingly
            incorrectPassword = (checkUser.password != request.POST['password'])
        except TypeError:
            # if there is no user with the given name, an exception is thrown, in which case, noUser is set to true
            noUser = True
        if noUser:
            # if the username does not yet exist, the user is returned to the login page.
            # a message field would be a good thing to implement so the reason login was not completed is explained
            # to the user
            return render(request, "login.html", {"error": "User does not exist"})
        elif incorrectPassword:
            # if the password is incorrect for the given name, the user is returned to the login page
            # a message field would be a good thing to implement so the reason login was not completed is explained
            # to the user
            return render(request, "login.html", {"error": "Incorrect Password"})
        else:
            # if no issues are found, the user is redirected and the request.session["username"] field is set to the
            # username of the user
            request.session["username"] = checkUser.username
            request.session["user_type"] = checkUser.userType
            request.session["user_id"] = checkUser.userID
            return redirect("/home/")


class Home(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR", "INSTRUCTOR"]):
            return render(request, "home_supervisor&instructor.html")
        elif userAllowed(request, ["TA"]):
            return render(request, "view_users_instructor&TA.html", {"user_list": UserProfile.objects.all()})
        else:
            return redirect("/")


class SendNotification(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR", "INSTRUCTOR", "TA"]):
            return render(request, "send_notification.html", {"request.session.username": request.session["username"]})
        else:
            return redirect("/../")


class CreateUser(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name or if they are not of the type SUPERVISOR, they will fail
        # userAllowed and will be redirected to home
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "create_user.html", {})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        # Takes user input of all parameters and creates a new user.
        try:
            UserManagement.createUser(user_id=int(request.POST["userID"]), user_type=request.POST["userType"],
                                      username=request.POST["username"], password=request.POST["password"],
                                      name=request.POST["name"], address=request.POST["address"],
                                      phone=int(request.POST["phone"]), email=request.POST["email"])
            return render(request, "create_user.html")
        except (TypeError, ValueError) as e:
            return render(request, "create_user.html",
                          {"error": "User was not created. " + str(e)})


class CreateCourse(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name or if they are not of the type SUPERVISOR, they will fail
        # userAllowed and be redirected to home
        if userAllowed(request, ['SUPERVISOR']):
            return render(request, "create_course.html", {"UserProfile_list": UserProfile.objects.all()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        # Takes user input of all parameters and creates a new course.
        try:
            gottenTAs = request.POST.getlist("TAs")
            for i in range(len(gottenTAs)):
                gottenTAs[i] = UserProfile.objects.get(userID=int(gottenTAs[i]))
            gottenDays = request.POST.getlist("days")
            days = ""
            for i in range(len(gottenDays)):
                if i < len(gottenDays) - 1:
                    days = days + gottenDays[i] + ', '
                else:
                    days = days + gottenDays[i]
            CourseManagement.createCourse(course_id=int(request.POST['ID']), name=request.POST['name'],
                                          location=request.POST['location'], hours=request.POST['hours'],
                                          days=days,
                                          instructor=UserManagement.findUser(user_id=int(request.POST['instructor'])),
                                          tas=gottenTAs)
            return render(request, "create_course.html", {"UserProfile_list": UserProfile.objects.all()})
        except (TypeError, ValueError) as e:
            return render(request, "create_course.html", {"UserProfile_list": UserProfile.objects.all(),
                                                          "error": "Course was not created. " + str(e)})
        except MultiValueDictKeyError:
            return render(request, "create_course.html", {"UserProfile_list": UserProfile.objects.all(),
                                                          "error": "Course was not created. An instructor must be "
                                                                   "chosen"})


class AccountSettings(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR", "INSTRUCTOR", "TA"]):
            return render(request, "account_settings.html",
                          {"user": UserManagement.findUser(user_id=request.session["user_id"])})
        else:
            return redirect("/home")

    @staticmethod
    def post(request):
        try:
            edit = bool(request.POST["edit"])
            if edit:
                return render(request, "account_settings.html",
                              {"user": UserManagement.findUser(user_id=request.session["user_id"]), "edit": edit})
            else:
                UserManagement.editUser(user_id=int(request.POST["userID"]), username=request.POST["username"],
                                        password=request.POST["password"], name=request.POST["name"],
                                        address=request.POST["address"], phone=int(request.POST["phone"]),
                                        email=request.POST["email"])
                return render(request, "account_settings.html",
                              {"user": UserProfile.objects.get(userID=request.session["user_id"]), "edit": edit})
        except (TypeError, ValueError) as e:
            return render(request, "account_settings.html",
                          {"user": UserManagement.findUser(user_id=int(request.session["user_id"])), "edit": False,
                           "error": "User was not changed. " + str(e)})


class EditUser(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "edit_user.html", {"object_list": UserProfile.objects.all()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        try:
            edit = True
            try:
                user_id = int(request.POST["edit"])
            except MultiValueDictKeyError:
                user_id = int(request.POST["submit"])
                edit = False
            if edit:
                change_user = UserManagement.findUser(user_id=user_id)
                return render(request, "edit_user.html",
                              {"object_list": UserProfile.objects.all(), "change_user": change_user})
            else:
                UserManagement.editUser(user_id=user_id, user_type=request.POST["type"],
                                        username=request.POST["username"],
                                        name=request.POST["name"], address=request.POST["address"],
                                        phone=int(request.POST["phone"]), email=request.POST["email"])
                return render(request, "edit_user.html", {"object_list": UserProfile.objects.all()})
        except (TypeError, ValueError) as e:
            return render(request, "edit_user.html",
                          {"object_list": UserProfile.objects.all(), "error": "User was not changed. " + str(e)})


class EditCourse(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "edit_course.html", {"Course_list": Course.objects.all()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        edit = True
        try:
            try:
                course_id = request.POST["edit"]
            except MultiValueDictKeyError:
                course_id = request.POST["submit"]
                edit = False
            if edit:
                change_course = CourseManagement.findCourse(int(course_id))
                return render(request, "edit_course.html",
                              {"Course_list": Course.objects.all(), "change_course": change_course,
                               "UserProfile_list": UserProfile.objects.all()})
            else:
                gottenTAs = request.POST.getlist("TAs")
                for i in range(len(gottenTAs)):
                    gottenTAs[i] = UserProfile.objects.get(userID=int(gottenTAs[i]))
                gottenDays = request.POST.getlist("days")
                days = ""
                for i in range(len(gottenDays)):
                    if i < len(gottenDays) - 1:
                        days = days + gottenDays[i] + ', '
                    else:
                        days = days + gottenDays[i]
                change_course = CourseManagement.findCourse(course_id=int(course_id))
                CourseManagement.editCourse(int(change_course.courseID), name=request.POST["name"],
                                            location=request.POST["location"], days=days,
                                            hours=request.POST["hours"],
                                            instructor=UserProfile.objects.get(userID=int(request.POST["instructor"])),
                                            tas=gottenTAs)
                return render(request, "edit_course.html", {"Course_list": Course.objects.all()})
        except (TypeError, ValueError) as e:
            return render(request, "edit_course.html",
                          {"Course_list": Course.objects.all(), "error": "Course was not edited. " + str(e)})
        except MultiValueDictKeyError:
            return render(request, "create_course.html", {"UserProfile_list": UserProfile.objects.all(),
                                                          "error": "Course was not created. An instructor must be "
                                                                   "chosen"})


class DeleteLab(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "delete_lab.html", {"lab_list": Lab.objects.all()})
        elif userAllowed(request, ["INSTRUCTOR"]):
            return render(request, "delete_lab.html",
                          {"lab_list": UserManagement.findUser(user_id=int(request.session["user_id"])).getLabList()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        LabManagement.deleteLab(lab_id=int(request.POST["delete"]))
        currentUser = UserManagement.findUser(user_id=int(request.session["user_id"]))
        if currentUser.userType == "SUPERVISOR":
            return render(request, "delete_lab.html", {"lab_list": Lab.objects.all()})
        elif currentUser.userType == "INSTRUCTOR":
            return render(request, "delete_lab.html", {"lab_list": currentUser.getLabList()})


class DeleteCourse(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "delete_course.html", {"course_list": Course.objects.all()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        CourseManagement.deleteCourse(course_id=int(request.POST["delete"]))
        return render(request, "delete_course.html", {"course_list": Course.objects.all()})


class DeleteUser(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "delete_user.html", {"user_list": UserProfile.objects.all()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        try:
            UserManagement.deleteUser(user_id=int(request.POST["delete"]))
            return render(request, "delete_user.html", {"user_list": UserProfile.objects.all()})
        except ProtectedError:
            return render(request, "delete_user.html", {"user_list": UserProfile.objects.all(),
                                                        "error": "User was not deleted. Cannot delete an instructor "
                                                                 "that is still assigned to a course or a TA that is "
                                                                 "assigned to a particular lab section"})


class CreateLab(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "create_lab.html",
                          {"Course_list": Course.objects.all(), "UserProfile_list": UserProfile.objects.all()})
        elif userAllowed(request, ["INSTRUCTOR"]):
            ta_choices = []
            course_choices = []
            for course in UserManagement.findUser(user_id=int(request.session["user_id"])).course_set.all():
                course_choices.append(course)
                for ta in course.TAs.all():
                    ta_choices.append(ta)
            return render(request, "create_lab.html", {"Course_list": course_choices, "UserProfile_list": ta_choices})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        currentUser = UserProfile.objects.get(userID=int(request.session["user_id"]))
        if currentUser.userType == "INSTRUCTOR":
            ta_choices = []
            course_choices = []
            for course in UserManagement.findUser(user_id=int(request.session["user_id"])).course_set.all():
                course_choices.append(course)
                for ta in course.TAs.all():
                    ta_choices.append(ta)
        try:
            gottenDays = request.POST.getlist("labDays")
            days = ""
            for i in range(len(gottenDays)):
                if i < len(gottenDays) - 1:
                    days = days + gottenDays[i] + ', '
                else:
                    days = days + gottenDays[i]
            LabManagement.createLab(lab_id=int(request.POST['labID']), lab_name=request.POST['labName'],
                                    lab_hours=request.POST['labHours'], lab_location=request.POST['labLocation'],
                                    lab_days=days, course=Course.objects.get(courseID=int(request.POST['course'])),
                                    ta=UserProfile.objects.get(userID=int(request.POST['labTA'])))
            if currentUser.userType == "SUPERVISOR":
                return render(request, "create_lab.html",
                              {"Course_list": Course.objects.all(), "UserProfile_list": UserProfile.objects.all()})
            elif currentUser.userType == "INSTRUCTOR":
                return render(request, "create_lab.html",
                              {"Course_list": course_choices, "UserProfile_list": ta_choices})
        except (TypeError, ValueError, MultiValueDictKeyError) as e:
            if currentUser.userType == "SUPERVISOR":
                return render(request, "create_lab.html",
                              {"Course_list": Course.objects.all(), "UserProfile_list": UserProfile.objects.all(),
                               "error": "Lab section was not created. " + str(e)})
            elif currentUser.userType == "INSTRUCTOR":
                return render(request, "create_lab.html",
                              {"Course_list": course_choices, "UserProfile_list": ta_choices,
                               "error": "Lab section was not created " + str(e)})



class EditLab(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "edit_lab.html", {"object_list": Lab.objects.all()})
        if userAllowed(request, ["INSTRUCTOR"]):
            return render(request, "edit_lab.html", {
                "object_list": UserManagement.findUser(user_id=int(request.session["user_id"])).getLabList()})
        else:
            return redirect("/home/")

    @staticmethod
    def post(request):
        currentUser = UserManagement.findUser(user_id=int(request.session["user_id"]))
        ta_choices = []
        course_choices = []
        if currentUser.userType == "INSTRUCTOR":
            for course in UserManagement.findUser(user_id=int(request.session["user_id"])).course_set.all():
                course_choices.append(course)
                for ta in course.TAs.all():
                    if not (ta in ta_choices):
                        ta_choices.append(ta)
        try:
            edit = True
            try:
                lab_id = int(request.POST["edit"])
            except MultiValueDictKeyError:
                lab_id = int(request.POST["submit"])
                edit = False
            if edit:
                change_lab = Lab.objects.get(labID=lab_id)
                if currentUser.userType == "SUPERVISOR":
                    return render(request, "edit_lab.html",
                                  {"object_list": Lab.objects.all(), "Course_list": Course.objects.all(),
                                   "UserProfile_list": UserProfile.objects.all(), "change_lab": change_lab})
                elif currentUser.userType == "INSTRUCTOR":
                    return render(request, "edit_lab.html",
                                  {"object_list": currentUser.getLabList(), "Course_list": course_choices,
                                   "UserProfile_list": ta_choices, "change_lab": change_lab})
            else:
                gottenDays = request.POST.getlist("days")
                days = ""
                for i in range(len(gottenDays)):
                    if i < len(gottenDays) - 1:
                        days = days + gottenDays[i] + ', '
                    else:
                        days = days + gottenDays[i]
                LabManagement.editLab(lab_id=lab_id, lab_name=request.POST["name"],
                                      lab_location=request.POST["location"], lab_hours=request.POST["hours"],
                                      lab_days=days, course=Course.objects.get(courseID=int(request.POST["course"])),
                                      ta=UserManagement.findUser(user_id=int(request.POST["TA"])))
                if currentUser.userType == "SUPERVISOR":
                    return render(request, "edit_lab.html", {"object_list": Lab.objects.all()})
                elif currentUser.userType == "INSTRUCTOR":
                    return render(request, "edit_lab.html", {
                        "object_list": currentUser.getLabList()})
        except (TypeError, ValueError, MultiValueDictKeyError) as e:
            if currentUser.userType == "SUPERVISOR":
                return render(request, "edit_lab.html",
                              {"object_list": Lab.objects.all(), "error": "Lab section was not changed. " + str(e)})
            elif currentUser.userType == "INSTRUCTOR":
                return render(request, "edit_lab.html", {
                    "object_list": currentUser.getLabList(), "error": "Lab section was not changed. " + str(e)})


class ViewUsers(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "view_users_supervisor.html", {"user_list": UserProfile.objects.all()})
        elif userAllowed(request, ["INSTRUCTOR", "TA"]):
            return render(request, "view_users_instructor&TA.html", {"user_list": UserProfile.objects.all()})
        else:
            return redirect("/home")


class ViewCourses(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR"]):
            return render(request, "view_courses_supervisor.html", {"course_list": Course.objects.all()})
        elif userAllowed(request, ["INSTRUCTOR"]):
            return render(request, "view_courses_instructor.html", {"course_list": Course.objects.all()})
        else:
            return redirect("/home")


class ViewLabs(View):
    @staticmethod
    def get(request):
        # If the user does not have a valid name, I.E. if they try to manually enter /home in the search bar,
        # they will fail the userAllowed test and be redirected back to the login page
        # If the user is allowed then home is rendered like normal
        if userAllowed(request, ["SUPERVISOR", "INSTRUCTOR"]):
            return render(request, "view_labs_supervisor&instructor.html", {"lab_list": Lab.objects.all()})
        else:
            return redirect("/home")
