"""no_excuses_fitness URL Configuration

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

from . import admin_views, member_views, trainer_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("trainer/add", admin_views.add_trainer, name='add_trainer'),
    path("course/add", admin_views.add_work_out_plan, name='add_course'),
    path("send_member_notification/", admin_views.send_member_notification,
         name='send_member_notification'),
    path("send_trainer_notification/", admin_views.send_trainer_notification,
         name='send_trainer_notification'),
    path("add_session/", admin_views.add_session, name='add_session'),
    path("admin_notify_member", admin_views.admin_notify_member,
         name='admin_notify_member'),
    path("admin_notify_trainer", admin_views.admin_notify_trainer,
         name='admin_notify_trainer'),
    path("admin_view_profile", admin_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", admin_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", admin_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         admin_views.edit_session, name='edit_session'),
    path("member/view/feedback/", admin_views.member_feedback_message,
         name="member_feedback_message",),
    path("trainer/view/feedback/", admin_views.trainer_feedback_message,
         name="trainer_feedback_message",),
    path("member/view/leave/", admin_views.view_member_leave,
         name="view_member_leave",),
    path("trainer/view/leave/", admin_views.view_trainer_leave, name="view_trainer_leave",),
    path("attendance/view/", admin_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", admin_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("member/add/", admin_views.add_member, name='add_member'),
    path("subject/add/", admin_views.add_work_out_plan_exercise, name='add_subject'),
    path("trainer/manage/", admin_views.manage_trainer, name='manage_trainer'),
    path("member/manage/", admin_views.manage_member, name='manage_member'),
    path("course/manage/", admin_views.manage_work_out_plan, name='manage_course'),
    path("subject/manage/", admin_views.manage_work_out_plan_exercise, name='manage_subject'),
    path("trainer/edit/<int:trainer_id>", admin_views.edit_trainer, name='edit_trainer'),
    path("trainer/delete/<int:trainer_id>",
         admin_views.delete_trainer, name='delete_trainer'),

    path("course/delete/<int:course_id>",
         admin_views.delete_work_out_plan, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         admin_views.delete_work_out_plan_exercise, name='delete_subject'),

    path("session/delete/<int:session_id>",
         admin_views.delete_session, name='delete_session'),

    path("member/delete/<int:member_id>",
         admin_views.delete_member, name='delete_member'),
    path("member/edit/<int:member_id>",
         admin_views.edit_member, name='edit_member'),
    path("course/edit/<int:course_id>",
         admin_views.edit_work_out_plan, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         admin_views.edit_work_out_plan_exercise, name='edit_subject'),


    # trainer
    path("trainer/home/", trainer_views.trainer_home, name='trainer_home'),
    path("trainer/apply/leave/", trainer_views.trainer_apply_leave,
         name='trainer_apply_leave'),
    path("trainer/feedback/", trainer_views.trainer_feedback, name='trainer_feedback'),
    path("trainer/view/profile/", trainer_views.trainer_view_profile,
         name='trainer_view_profile'),
    path("trainer/attendance/take/", trainer_views.trainer_take_attendance,
         name='trainer_take_attendance'),
    path("trainer/attendance/update/", trainer_views.trainer_update_attendance,
         name='trainer_update_attendance'),
    path("trainer/get_members/", trainer_views.get_members, name='get_members'),
     path("trainer/addbook/", trainer_views.add_suppliment, name="add_book"),
    path("trainer/issue_book/", trainer_views.issue_suppliment, name="issue_book"),
    path("trainer/view_issued_book/", trainer_views.view_issued_suppliment, name="view_issued_book"),



    path("trainer/attendance/fetch/", trainer_views.get_member_attendance,
         name='get_member_attendance'),
    path("trainer/attendance/save/",
         trainer_views.save_attendance, name='save_attendance'),
    path("trainer/attendance/update/",
         trainer_views.update_attendance, name='update_attendance'),
    path("trainer/fcmtoken/", trainer_views.trainer_fcmtoken, name='trainer_fcmtoken'),
    path("trainer/view/notification/", trainer_views.trainer_view_notification,
         name="trainer_view_notification"),
    path("trainer/result/add/", trainer_views.trainer_add_result, name='trainer_add_result'),
    path("trainer/result/edit/", EditResultView.as_view(),
         name='edit_member_result'),
    path('trainer/result/fetch/', trainer_views.fetch_member_result,
         name='fetch_member_result'),



    # member
    path("member/home/", member_views.member_home, name='member_home'),
    path("member/view/attendance/", member_views.member_view_attendance,
         name='member_view_attendance'),
    path("member/apply/leave/", member_views.member_apply_leave,
         name='member_apply_leave'),
    path("member/feedback/", member_views.member_feedback,
         name='member_feedback'),
    path("member/view/profile/", member_views.member_view_profile,
         name='member_view_profile'),
    path("member/fcmtoken/", member_views.member_fcmtoken,
         name='member_fcmtoken'),
     # path('member/todo',member_views.todo,name='todo'),

     
     path("member/viewbooks/", member_views.view_suppliments, name="view_books"),

    path("member/view/notification/", member_views.member_view_notification,
         name="member_view_notification"),
    path('member/view/result/', member_views.member_view_result,
         name='member_view_result'),

]
