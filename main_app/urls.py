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

# from main_app.EditResultView import EditResultView

from . import admin_views, hr_views, employee_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("hr/add", admin_views.add_hr, name='add_hr'),
    path("designation/add", admin_views.add_designation, name='add_designation'),
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
    path("project/add/", admin_views.add_project, name='add_project'),
    path("hr/manage/", admin_views.manage_hr, name='manage_hr'),
    path("employee/manage/", admin_views.manage_employee, name='manage_employee'),
    path("designation/manage/", admin_views.manage_designation, name='manage_designation'),
    path("project/manage/", admin_views.manage_project, name='manage_project'),
    path("hr/edit/<int:hr_id>", admin_views.edit_hr, name='edit_hr'),
    path("hr/delete/<int:hr_id>",
         admin_views.delete_hr, name='delete_hr'),

    path("designation/delete/<int:designation_id>",
         admin_views.delete_designation, name='delete_designation'),

    path("project/delete/<int:project_id>",
         admin_views.delete_project, name='delete_project'),

    path("session/delete/<int:session_id>",
         admin_views.delete_session, name='delete_session'),

    path("employee/delete/<int:employee_id>",
         admin_views.delete_employee, name='delete_employee'),
    path("employee/edit/<int:employee_id>",
         admin_views.edit_employee, name='edit_employee'),
    path("designation/edit/<int:designation_id>",
         admin_views.edit_designation, name='edit_designation'),
    path("project/edit/<int:project_id>",
         admin_views.edit_project, name='edit_project'),


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
     path("hr/addasset/", hr_views.add_asset, name="add_asset"),
    path("hr/issue_asset/", hr_views.issue_asset, name="issue_asset"),
    path("hr/view_issued_asset/", hr_views.view_issued_asset, name="view_issued_asset"),



    path("hr/attendance/fetch/", hr_views.get_employee_attendance,
         name='get_employee_attendance'),
    path("hr/attendance/save/",
         hr_views.save_attendance, name='save_attendance'),
    path("hr/attendance/update/",
         hr_views.update_attendance, name='update_attendance'),
    path("hr/fcmtoken/", hr_views.hr_fcmtoken, name='hr_fcmtoken'),
    path("hr/view/notification/", hr_views.hr_view_notification,
         name="hr_view_notification"),
#     path("hr/result/add/", hr_views.hr_add_result, name='hr_add_result'),
#     path("hr/result/edit/", EditResultView.as_view(),
#          name='edit_employee_result'),
#     path('hr/result/fetch/', hr_views.fetch_employee_result,
#          name='fetch_employee_result'),



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

     
     path("employee/viewassets/", employee_views.view_assets, name="view_assets"),

    path("employee/view/notification/", employee_views.employee_view_notification,
         name="employee_view_notification"),
#     path('employee/view/result/', employee_views.employee_view_result,
#          name='employee_view_result'),

]
