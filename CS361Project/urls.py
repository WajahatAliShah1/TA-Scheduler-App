"""CS361Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from TAScheduler.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('home/', Home.as_view()),
    path('send_notification/', SendNotification.as_view()),
    path('create_user/', CreateUser.as_view()),
    path('create_course/', CreateCourse.as_view()),
    path('create_lab/', CreateLab.as_view()),
    path('account_settings/', AccountSettings.as_view()),
    path('edit_user/', EditUser.as_view()),
    path('edit_course/', EditCourse.as_view()),
    path('delete_course/', DeleteCourse.as_view()),
    path('delete_user/', DeleteUser.as_view()),
    path('edit_lab/', EditLab.as_view()),
    path('delete_lab/', DeleteLab.as_view()),
    path('view_users/', ViewUsers.as_view()),
    path('view_courses/', ViewCourses.as_view()),
    path('view_labs/', ViewLabs.as_view()),
]
