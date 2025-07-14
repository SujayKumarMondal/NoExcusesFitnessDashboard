"""teamOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from main_app.EditResultView import EditResultView

from . import admin_views, hr_views, employee_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("hr/add", admin_views.add_hr, name='add_hr'),
    path("course/add", admin_views.add_course, name='add_course'),
    path("send_employee_notification/", admin_views.send_employee_notification,
         name='send_employee_notification'),
    path("send_hr_notification/", admin_views.send_hr_notification,
         name='send_hr_notification'),
    path("add_session/", admin_views.add_session, name='add_session'),
    path("admin_notify_employee", admin_views.admin_notify_employee,
         name='admin_notify_employee'),
    path("admin_notify_hr", admin_views.admin_notify_hr,
         name='admin_notify_hr'),
    path("admin_view_profile", admin_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", admin_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", admin_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         admin_views.edit_session, name='edit_session'),
    path("employee/view/feedback/", admin_views.employee_feedback_message,
         name="employee_feedback_message",),
    path("hr/view/feedback/", admin_views.hr_feedback_message,
         name="hr_feedback_message",),
    path("employee/view/leave/", admin_views.view_employee_leave,
         name="view_employee_leave",),
    path("hr/view/leave/", admin_views.view_hr_leave, name="view_hr_leave",),
    path("attendance/view/", admin_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", admin_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("employee/add/", admin_views.add_employee, name='add_employee'),
    path("subject/add/", admin_views.add_subject, name='add_subject'),
    path("hr/manage/", admin_views.manage_hr, name='manage_hr'),
    path("employee/manage/", admin_views.manage_employee, name='manage_employee'),
    path("course/manage/", admin_views.manage_course, name='manage_course'),
    path("subject/manage/", admin_views.manage_subject, name='manage_subject'),
    path("hr/edit/<int:hr_id>", admin_views.edit_hr, name='edit_hr'),
    path("hr/delete/<int:hr_id>",
         admin_views.delete_hr, name='delete_hr'),

    path("course/delete/<int:course_id>",
         admin_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         admin_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         admin_views.delete_session, name='delete_session'),

    path("employee/delete/<int:employee_id>",
         admin_views.delete_employee, name='delete_employee'),
    path("employee/edit/<int:employee_id>",
         admin_views.edit_employee, name='edit_employee'),
    path("course/edit/<int:course_id>",
         admin_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         admin_views.edit_subject, name='edit_subject'),


    # hr
    path("hr/home/", hr_views.hr_home, name='hr_home'),
    path("hr/apply/leave/", hr_views.hr_apply_leave,
         name='hr_apply_leave'),
    path("hr/feedback/", hr_views.hr_feedback, name='hr_feedback'),
    path("hr/view/profile/", hr_views.hr_view_profile,
         name='hr_view_profile'),
    path("hr/attendance/take/", hr_views.hr_take_attendance,
         name='hr_take_attendance'),
    path("hr/attendance/update/", hr_views.hr_update_attendance,
         name='hr_update_attendance'),
    path("hr/get_employees/", hr_views.get_employees, name='get_employees'),
     path("hr/addbook/", hr_views.add_book, name="add_book"),
    path("hr/issue_book/", hr_views.issue_book, name="issue_book"),
    path("hr/view_issued_book/", hr_views.view_issued_book, name="view_issued_book"),



    path("hr/attendance/fetch/", hr_views.get_employee_attendance,
         name='get_employee_attendance'),
    path("hr/attendance/save/",
         hr_views.save_attendance, name='save_attendance'),
    path("hr/attendance/update/",
         hr_views.update_attendance, name='update_attendance'),
    path("hr/fcmtoken/", hr_views.hr_fcmtoken, name='hr_fcmtoken'),
    path("hr/view/notification/", hr_views.hr_view_notification,
         name="hr_view_notification"),
    path("hr/result/add/", hr_views.hr_add_result, name='hr_add_result'),
    path("hr/result/edit/", EditResultView.as_view(),
         name='edit_employee_result'),
    path('hr/result/fetch/', hr_views.fetch_employee_result,
         name='fetch_employee_result'),



    # employee
    path("employee/home/", employee_views.employee_home, name='employee_home'),
    path("employee/view/attendance/", employee_views.employee_view_attendance,
         name='employee_view_attendance'),
    path("employee/apply/leave/", employee_views.employee_apply_leave,
         name='employee_apply_leave'),
    path("employee/feedback/", employee_views.employee_feedback,
         name='employee_feedback'),
    path("employee/view/profile/", employee_views.employee_view_profile,
         name='employee_view_profile'),
    path("employee/fcmtoken/", employee_views.employee_fcmtoken,
         name='employee_fcmtoken'),
     # path('employee/todo',employee_views.todo,name='todo'),

     
     path("employee/viewbooks/", employee_views.view_books, name="view_books"),

    path("employee/view/notification/", employee_views.employee_view_notification,
         name="employee_view_notification"),
    path('employee/view/result/', employee_views.employee_view_result,
         name='employee_view_result'),

]
