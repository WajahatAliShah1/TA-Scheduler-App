from TAScheduler.models import *
import re


class LabManagement(object):

    # Preconditions: The user has to have been instantiated.
    #   The user must be of type administrator
    # Postconditions: Creates a lab
    #   The lab must be connected to an already instantiated course
    # Side-effects: Lab is created and added inside the database
    # Lab ID(in) - ID of the lab
    # Lab Name(in) - Name of the lab
    # Lab Hours(in) - Hours of the lab
    # Lab Location(in) - Location of the lab
    # Lab Days(in) - Days of the lab
    # Lab Course(in) - Course associated with the lab
    # Lab TA(in) -TA of the lab
    @staticmethod
    def createLab(lab_id, lab_name, lab_location, lab_hours, lab_days, course, ta):
        LabManagement.__inputErrorCheck(lab_id, lab_name, lab_location, lab_hours, lab_days, course, ta)
        if Lab.objects.filter(labID=lab_id).exists():
            raise TypeError("That labID is already in use")
        Lab.objects.create(labID=lab_id, name=lab_name, location=lab_location, hours=lab_hours, days=lab_days,
                           course=course, TA=ta)

    # Preconditions: The user has to have been instantiated.
    #   The user must be of type administrator
    # Postconditions:Edits a lab
    #   The lab must be connected to an already instantiated course
    # Side-effects: Lab is edited inside the database
    # Lab ID(in) - ID of the lab
    # Lab Name(in) - Name of the lab
    # Lab Hours(in) - Hours of the lab
    # Lab Location(in) - Location of the lab
    # Lab Days(in) - Days of the lab
    # Lab Course(in) - Course associated with the lab
    # Lab TA(in) -TA of the lab
    @staticmethod
    def editLab(lab_id=None, lab_name=None, lab_location=None, lab_hours=None, lab_days=None, course=None, ta=None):
        LabManagement.__inputErrorCheck(lab_id=lab_id, name=lab_name, hours=lab_hours, location=lab_location,
                                        days=lab_days, course=course, ta=ta)
        if not (Lab.objects.filter(labID=lab_id).exists()):
            raise TypeError("This Lab does not exist")

        editedLab = Lab.objects.get(labID=lab_id)
        if not (lab_name is None):
            editedLab.name = lab_name
        if not (lab_location is None):
            editedLab.location = lab_location
        if not (lab_hours is None):
            editedLab.hours = lab_hours
        if not (lab_days is None):
            editedLab.days = lab_days
        if not (course is None):
            if not (ta is None):
                if not (course in editedLab.TA.TAToCourse.all()):
                    raise ValueError("A lab's course cannot be changed if the lab TA is not assigned to that course")
                elif not (course in ta.TAToCourse.all()):
                    raise ValueError("A lab's course cannot be changed if the lab TA is not assigned to that course")
            editedLab.course = course
        if not (ta is None):
            editedLab.TA = ta
        editedLab.save()

        return "The lab was successfully edited"

    # Preconditions: The user has to have been instantiated.
    # The user must be of type administrator
    # Postconditions:Deletes a lab
    # Side-effects: Lab is deleted and removed from the database
    # Lab ID(in) - ID of the lab
    @staticmethod
    def deleteLab(lab_id):
        LabManagement.__inputErrorCheck(lab_id=lab_id)
        try:
            Lab.objects.get(labID=lab_id).delete()
        except Lab.DoesNotExist:
            raise ValueError("The course_id provided does not exist")

    @staticmethod
    def __inputErrorCheck(lab_id=None, name=None, location=None, hours=None, days=None, course=None, ta=None):
        if not (lab_id is None):
            if not (isinstance(lab_id, int)):
                raise TypeError("lab_id entered is not of type int")
        if not (name is None):
            if not (isinstance(name, str)):
                raise TypeError("Lab Name entered is not of type str")
            if not (len(name) > 0):
                raise ValueError("Name should not be left blank")
        if not (location is None):
            if not (isinstance(location, str)):
                raise TypeError("Lab Location entered is not of type str")
            if not (len(location) > 0):
                raise ValueError("Location should not be left blank")
        if not (hours is None):
            if not (isinstance(hours, str)):
                raise TypeError("Lab Hours entered is not of type str")
            if not (len(hours) > 0):
                raise ValueError("Hours should not be left blank")
            if not (bool(re.match("([1][0-2]|[0][1-9]):([0-5][0-9]) ([AP])M - ([1][0-2]|[0][1-9]):([0-5][0-9]) ([AP])M",
                                  hours))):
                raise ValueError("Wrong format for hours. Format should be HH:MM AM/PM - HH:MM AM/PM")
        if not (days is None):
            if not (isinstance(days, str)):
                raise TypeError("Lab Days entered is not of type str")
            if not (len(days) > 0):
                raise ValueError("At least one day must be selected")
            if not (bool(re.match("[MTW(Th)F],*", days))):
                raise ValueError("Wrong format for days. Format should be first letters of days separated by commas "
                                 "with Th for Thursday")
        if not (course is None):
            if not (isinstance(course, Course)):
                raise TypeError("Course entered is not of type course")
        if not (ta is None):
            if not (isinstance(ta, UserProfile)):
                raise TypeError("Lab TA entered is not of type User")
            if ta.userType != "TA":
                raise TypeError("Lab TA's type is not of type TA")
            if not (course is None):
                if not (course in ta.TAToCourse.all()):
                    raise ValueError("TAs cannot be assigned to labs for courses they are not assigned to")
