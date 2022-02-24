# createCourse(name, courseTime, days, hours, instructor, courseTA)
# editCourse(name, courseTime, days, hours, instructor, courseTa)
# deleteCourse(name)
# populateSearchClass(searchPromp)  should change class to course
# displayAllCourse()
from TAScheduler.models import *
import re


class CourseManagement(object):

    # Preconditions: The user has to have been instantiated.
    #                The user must be of type administrator
    # Postconditions:Creates a course
    # Side-effects: Course is created and added inside the database
    # Course ID(in) - Id of the courses
    # Course Name(in) - Name of the course
    # Course Location(in) - Location of the course
    # Course Days(in) - Days of the course
    # Course Hours(in) - Hours of the course
    # Course Instructor(in) - Instructor of the course
    # Course TAs(in) -TAs of the course
    @staticmethod
    def createCourse(course_id, name, location, days, hours, instructor, tas=None):
        CourseManagement.inputErrorChecker(course_id, name, location, days, hours, instructor, tas)
        try:
            Course.objects.get(courseID=course_id)
        except Course.DoesNotExist:
            Course.objects.create(courseID=course_id, name=name, location=location, hours=hours, days=days,
                                  instructor=instructor)
            course = Course.objects.get(courseID=course_id)
            if not (tas is None):
                for ta in tas:
                    course.TAs.add(ta)
            return
        raise TypeError("The course_id entered already exists")

    # Preconditions: The user has to have been instantiated.
    # The user must be of type administrator
    # Postconditions:Edits a course
    # Side-effects: Course is edited inside the database
    # Course ID(in) - Id of the courses
    # Course Name(in) - Name of the course
    # Course Location(in) - Location of the course
    # Course Days(in) - Days of the course
    # Course Hours(in) - Hours of the course
    # Course Instructor(in) - Instructor of the Course
    @staticmethod
    def editCourse(course_id, name=None, location=None, days=None, hours=None, instructor=None, tas=None):
        CourseManagement.inputErrorChecker(course_id, name, location, days, hours, instructor, tas)
        if not (Course.objects.filter(courseID=course_id).exists()):
            raise TypeError("This course does not exist")

        editedCourse = Course.objects.get(courseID=course_id)
        if not (name is None):
            editedCourse.name = name
        if not (location is None):
            editedCourse.location = location
        if not (hours is None):
            editedCourse.hours = hours
        if not (days is None):
            editedCourse.days = days
        if not (instructor is None):
            editedCourse.instructor = instructor
        if not (tas is None):
            editedCourse.TAs.clear()
            for i in tas:
                editedCourse.TAs.add(i)
        editedCourse.save()

    # Preconditions: The user has to have been instantiated.
    #                The user must be of type administrator
    # Postconditions:Finds a course
    # Side-effects: None
    # CourseID(in) - ID of the course
    # Course(out) - Course Found
    @staticmethod
    def findCourse(course_id):
        course = Course
        if not (course_id == 0):
            CourseManagement.inputErrorChecker(course_id=course_id)
            try:
                course = Course.objects.get(courseID=course_id)
            except Course.DoesNotExist:
                raise TypeError("This ID does not exist")
        return course

    # Preconditions: The user has to have been instantiated.
    # The user must be of type administrator
    # Postconditions:Deletes a course
    # Side-effects: Course is deleted and removed from the database
    # Course ID(in) - ID of the course
    @staticmethod
    def deleteCourse(course_id):
        CourseManagement.inputErrorChecker(course_id=course_id)
        try:
            Course.objects.get(courseID=course_id).delete()
        except Course.DoesNotExist:
            raise ValueError("The course_id provided does not exist")

    @staticmethod
    def inputErrorChecker(course_id=None, name=None, location=None, days=None, hours=None, instructor=None, tas=None):
        if not (course_id is None):
            if not (isinstance(course_id, int)):
                raise TypeError("course_id entered is not of type int")
        if not (name is None):
            if not (isinstance(name, str)):
                raise TypeError("Course name entered is not of type str")
            if not (len(name) > 0):
                raise ValueError("Name should not be left blank")
        if not (location is None):
            if not (isinstance(location, str)):
                raise TypeError("Course location entered is not of type str")
            if not (len(location) > 0):
                raise ValueError("Location should not be left blank")
        if not (days is None):
            if not (isinstance(days, str)):
                raise TypeError("Course hours entered is not of type str")
            if not (len(days) > 0):
                raise ValueError("At least one day must be selected")
            if not (bool(re.match("[MTW(Th)F],*", days))):
                raise ValueError("Wrong format for days. Format should be first letters of days separated by commas "
                                 "with Th for Thursday")
        if not (hours is None):
            if not (isinstance(hours, str)):
                raise TypeError("Course days entered is not of type str")
            if not (len(hours) > 0):
                raise ValueError("Hours should not be left blank")
            if not (bool(re.match("([1][0-2]|[0][1-9]):([0-5][0-9]) ([AP])M - ([1][0-2]|[0][1-9]):([0-5][0-9]) ([AP])M",
                                  hours))):
                raise ValueError("Wrong format for hours. Format should be HH:MM AM/PM - HH:MM AM/PM")
        if not (instructor is None):
            if not (isinstance(instructor, UserProfile)):
                raise TypeError("Course instructor entered is not of type User")
            if instructor.userType != "INSTRUCTOR":
                raise TypeError("Course instructor's type is not of type INSTRUCTOR")
        if not (tas is None):
            for TA in tas:
                if not (isinstance(TA, UserProfile)):
                    raise TypeError("Course TA entered is not of type User")
                if TA.userType != "TA":
                    raise TypeError("Course TA's type is not of type TA")
