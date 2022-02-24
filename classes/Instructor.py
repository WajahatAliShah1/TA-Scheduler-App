# from TAScheduler.models import UserProfile
#
# # userID = models.IntegerField(default=0)
# # userType = models.CharField(max_length=20, choices=[('SUPERVISOR', 'Supervisor'), ('INSTRUCTOR', 'Instructor'), ('TA', 'TA')])
# # userPassword = models.CharField(max_length=20)
# # userName = models.CharField(max_length=20)
# # userAddress = models.CharField(max_length=20)
# # userContact = models.IntegerField(default=0)
# # userEmail = models.CharField(max_length=20)
#
# class Instructor:
#     def __init__(self, id, name, contact):
#         self.id = id
#         pass
#
#     def assign_course(self, TA_ref, section_id):
#         # 1. filter out all the TAs
#         filtered_TA = UserProfile.objects.filter(userType='TA', userName='toy_ta')
#         Course.objects.update(section=section_id, )
#         pass
#
#     def retrieve_all_TAs(self):
#         passs
#
#         from TAScheduler.models import UserProfile
#
#         # userID = models.IntegerField(default=0)
#         # userType = models.CharField(max_length=20, choices=[('SUPERVISOR', 'Supervisor'), ('INSTRUCTOR', 'Instructor'), ('TA', 'TA')])
#         # userPassword = models.CharField(max_length=20)
#         # userName = models.CharField(max_length=20)
#         # userAddress = models.CharField(max_length=20)
#         # userContact = models.IntegerField(default=0)
#         # userEmail = models.CharField(max_length=20)
#
#         # methods required
#         # '''
#         # setId()
#         # setName()
#         # setContact()
#         # setSSN()
#         # setAddress()
#         # setPassword()
#         # setType()
#         # getType()
#         # getId()
#         # getName()
#         # getContact()
#         # getSSN()
#         # getAddress()
#         # getPassword()
#         # '''
#
#         '''
#         So I believe there are a few  changes we need to have.
#
#         Whenever a user is created, it should probably be a common convention that everything entered upon creation.
#         AT A MINIMUM, a user should be instantiated with their Name and SSN. Reason for this: having at least 2 fields entered
#         for a new user allows for easier use of filtering out a particular user to update their information or set
#         userType, contact info, etc....
#         '''
#
#         class userManagement:
#             def __init__(self, userID, userType, userPassword, userName, userAddress, userContact, userEmail):
#                 self.userID = userID
#                 self.userType = userType
#                 self.userPassword = userPassword
#                 self.userName = userName
#                 self.userAddress = userAddress
#                 self.userContact = userContact
#                 self.userEmail = userEmail
#
#                 newUser = UserProfile(self.userID, self.userType, self.userPassword, self.userName, self.userAddress,
#                                       self.userContact, self.userEmail)
#                 newUser.save()
#                 pass
#
#             def setId(self, ID, Name, SSN):
#                 # To set an ID for a user, you have to know their name and their SSN since you could have
#                 # multiple users with the same name
#                 filtered_User = UserProfile.objects.filter(userName=Name, userSSN=SSN)
#                 filtered_User.update(userID=ID)
#                 pass
#
#             def setName(self, ID, Name, SSN):
#                 # To set an name for a user, you have to know their ID or their SSN since you could have
#                 # multiple users with the same name
#                 filtered_User = UserProfile.objects.filter(userName=Name, userSSN=SSN)
#                 filtered_User.update(userName=Name)
#                 pass
#
#             def setContact(self):
#
#             def setSSN(self):
#
#             def setAddress(self):
#
#             def setPassword(self):
#                 filtered_User = UserProfile.objects.filter(userID="userID")
#                 filtered_User.update(userType=Type)
#                 pass
#
#             def setType(self, Type, userID):
#                 filtered_User = UserProfile.objects.filter(userID="userID")
#                 filtered_User.update(userType=Type)
#                 pass
#
#             def getType(self):
#
#             def getId(self):
#
#             def getName(self):
#
#             def getContact(self):
#
#             def getSSN(self):
#
#             def getAddress(self):
#
#             def getPassword(self):
#
#         # def assign_course(self, TA_ref, section_id):
#         #     # 1. filter out all the TAs
#         #     filtered_TA = UserProfile.objects.filter(userType='TA', userName='toy_ta')
#         #     Course.objects.update(section=section_id, )
#         #     pass
#         #
#         # def retrieve_all_TAs(self):
#         #     passs