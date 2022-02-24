from django.db import models

# Create your models here.


# UserProfile acts as the class that will be used for all users with the userType variable determining whether they
# are an instructor, TA, or Administrator
class UserProfile(models.Model):
    userID = models.IntegerField(default=0)
    userType = models.CharField(max_length=20,
                                choices=[('SUPERVISOR', 'Supervisor'), ('INSTRUCTOR', 'Instructor'), ('TA', 'TA')])
    username = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    phone = models.IntegerField(default=0)
    email = models.EmailField(max_length=30)

    def __str__(self):
        if len(self.username) == 0:
            return "Blank"
        return self.username

    def getCourseLabList(self):
        course_lab_list = []
        if self.userType == "INSTRUCTOR":
            for course in self.course_set.all():
                course_lab_list.append(course)
                for lab in course.lab_set.all():
                    course_lab_list.append(lab)
        elif self.userType == "TA":
            for course in self.TAToCourse.all():
                course_lab_list.append(course)
            for lab in self.TAToLab.all():
                course_lab_list.append(lab)
        course_lab_list.sort(key=UserProfile.mySort)
        return course_lab_list

    def getLabList(self):
        lab_list = []
        if self.userType == "INSTRUCTOR":
            for course in self.course_set.all():
                for lab in course.lab_set.all():
                    lab_list.append(lab)
        elif self.userType == "TA":
            for lab in self.TAToLab.all():
                lab_list.append(lab)
        return lab_list

    @staticmethod
    def mySort(lab_or_course):
        hours = lab_or_course.hours[: lab_or_course.hours.find(':')]
        if hours == "12":
            hours = "0"
        minutes = lab_or_course.hours[lab_or_course.hours.find(':') + 1: lab_or_course.hours.find(':') + 2]
        hours_and_minutes = hours + "." + minutes
        if lab_or_course.hours[lab_or_course.hours.find(':') + 4: lab_or_course.hours.find(':') + 6] == "AM":
            return float(hours_and_minutes) - 12
        elif lab_or_course.hours[lab_or_course.hours.find(':') + 4: lab_or_course.hours.find(':') + 6] == "PM":
            return float(hours_and_minutes)
        else:
            raise Exception("Formatting error with time of " + lab_or_course.name)


# The Course class keeps track of lecture sections and stores the TAs, instructors, and labs associated with it.
class Course(models.Model):
    courseID = models.IntegerField()
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    days = models.CharField(max_length=20)
    instructor = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    TAs = models.ManyToManyField(UserProfile, related_name="TAToCourse")

    def __str__(self):
        return self.name

    def getDays(self):
        day_list = []
        for i in range(len(self.days)):
            if self.days[i] == 'M':
                day_list.append('M')
            elif self.days[i] == 'T':
                try:
                    if self.days[i + 1] == 'h':
                        day_list.append('Th')
                    else:
                        day_list.append('T')
                except IndexError:
                    day_list.append('T')
            elif self.days[i] == 'W':
                day_list.append('W')
            elif self.days[i] == 'F':
                day_list.append('F')
            else:
                pass
        return day_list

    # class Meta:
    #     db_table = "CourseList"


# The Lab class keeps track of the information for a particular lab section and references the instructor of the
# course to keep track of which course it relates to.
class Lab(models.Model):
    labID = models.IntegerField()
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    days = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="TAToLab")

    def __str__(self):
        return self.course.name + ": " + self.name

    def getDays(self):
        return Course.getDays(self)
