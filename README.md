# TA-Scheduler-App

### About the Web App:
   This is a web application written in Python and built using the Django Framework. It incorporates user accounts, and makes use of the built in database to store and update information. We implemented a schedule viewing page, for every user, along with an accompanying courses/labs/account settings page as well as viewing information of other users depending on your user role. Each role has access to different permissions and pages to make certain changes, these are listed below.

#### The users of the application will have 3 roles:
   #### Supervisor/Administrator (department chair)
    -create courses
    -create accounts
    -delete accounts
    -edit accounts
    -send out notifications to users via UWM email
    -access all data in the system
    -assign instructors to courses
    -assign TAs to courses (usually specifying number of labs, or grader status)
    -assign TAs to particular lab sections
  #### Instructor
    -edit their own contact information (not course assignments)
    -view course assignments
    -view TA assignments (for all TAs)
    -send out notifications to their TAs via UWM email
    -assign their TAs to particular lab sections
    -read public contact information of all users
  #### TA
    -edit their own contact information (not course assignments)
    -view TA assignments (for all TAs)
    -read public contact information of all users

    Public information: the personal phone number or home address of a TA or instructor is private information. 
    The administrator and supervisor need to have access to it, but it is not available to other users.

### To run the project:
  1. Clone the repository to your local machine.
  2. Use VS-Code with the appropriate python/django extensions installed.
  3. Run the project and click on the local host url in terminal to navigate, and store/update information such as courses, labs, and account settings.
