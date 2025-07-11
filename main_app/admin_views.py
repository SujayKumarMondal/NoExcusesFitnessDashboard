import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *

# For Admins
def admin_home(request):
    total_trainers = Trainer.objects.all().count()
    total_members = Member.objects.all().count()
    work_out_plans = WorkoutPlanExercise.objects.all()
    total_work_out_plan = work_out_plans.count()
    total_work_out = WorkoutPlan.objects.all().count()
    attendance_list = Attendance.objects.filter(work_out_plan__in=work_out_plans)
    total_attendance = attendance_list.count()
    attendance_list = []
    work_out_plan_list = []
    for wop in work_out_plans:
        attendance_count = Attendance.objects.filter(wop=wop).count()
        work_out_plan_list.append(WorkoutPlanExercise.name[:7])
        attendance_list.append(attendance_count)

    # Total Subjects and members in Each Course
    work_out_all = WorkoutPlan.objects.all()
    work_out_name_list = []
    work_out_plan_count_list = []
    member_count_list_in_wope = []

    for woa in work_out_all:
        work_out_plans = WorkoutPlanExercise.objects.filter(id=woa.id).count()
        members = Member.objects.filter(id=woa.id).count()
        work_out_name_list.append(woa.work_out)
        work_out_plan_count_list.append(work_out_plans)
        member_count_list_in_wope.append(members)
    
    work_out_plan_all = WorkoutPlanExercise.objects.all()
    work_out_plan_list = []
    member_count_list_in_wop = []
    for wopa in work_out_plan_all:
        wop = WorkoutPlan.objects.get(id=wopa.plan.id)
        member_count = Member.objects.filter(id=wopa.id).count()
        work_out_plan_list.append(wopa.name)
        member_count_list_in_wop.append(member_count)


    # For Members
    member_attendance_present_list=[]
    member_attendance_leave_list=[]
    member_name_list=[]

    members = Member.objects.all()
    for mem in members:
        
        attendance = AttendanceReport.objects.filter(member_id=mem.id, status=True).count()
        absent = AttendanceReport.objects.filter(member_id=mem.id, status=False).count()
        leave = LeaveReportMember.objects.filter(member_id=mem.id, status=1).count()
        member_attendance_present_list.append(attendance)
        member_attendance_leave_list.append(leave+absent)
        member_name_list.append(Member.member.first_name)

    context = {
        'page_title': "NoExcusesFitness(Administrative Dashboard)",
        'total_members': total_members,
        'total_trainers': total_trainers,
        'total_work_out': total_work_out,
        'total_work_out_plan': total_work_out_plan,
        'work_out_plan_list': work_out_plan_list,
        'attendance_list': attendance_list,
        'member_attendance_present_list': member_attendance_present_list,
        'member_attendance_leave_list': member_attendance_leave_list,
        "member_name_list": member_name_list,
        "member_count_list_in_work_out_plan_exercise": member_count_list_in_wope,
        "member_count_list_in_work_out_plan": member_count_list_in_wop,
        "work_out_plan_name_list": work_out_name_list,

    }
    return render(request, 'admin_template/home_content.html', context)


def add_trainer(request):
    form = TrainerForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Trainer'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            work_out = form.cleaned_data.get('work_out')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.trainer.work_out = work_out
                user.save()
                messages.success(request, "Successfully Added Trainer")
                return redirect(reverse('add_trainer'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'admin_template/add_trainer_template.html', context)


def add_member(request):
    member_form = MemberForm(request.POST or None, request.FILES or None)
    context = {'form': member_form, 'page_title': 'Add Member'}
    if request.method == 'POST':
        if member_form.is_valid():
            first_name = member_form.cleaned_data.get('first_name')
            last_name = member_form.cleaned_data.get('last_name')
            address = member_form.cleaned_data.get('address')
            email = member_form.cleaned_data.get('email')
            gender = member_form.cleaned_data.get('gender')
            password = member_form.cleaned_data.get('password')
            work_out = member_form.cleaned_data.get('work_out')
            session = member_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.member.session = session
                user.member.work_out = work_out
                user.save()
                messages.success(request, "Successfully Added Member")
                return redirect(reverse('add_member'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'admin_template/add_member_template.html', context)


def add_work_out_plan(request):
    form = WorkoutPlanForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Work Out Plan'
    }
    if request.method == 'POST':
        if form.is_valid():
            work_out = form.cleaned_data.get('work_out')
            try:
                wop = WorkoutPlan()
                wop.work_out = work_out
                wop.save()
                messages.success(request, "Successfully Added Work Out Plan")
                return redirect(reverse('add_work_out_plan'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin_template/add_workout_plan_template.html', context)


def add_work_out_plan_exercise(request):
    form = WorkoutPlanExerciseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Work Out Plan Exercise'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            plan = form.cleaned_data.get('plan')
            trainer = form.cleaned_data.get('trainer')
            try:
                work_out_plan = WorkoutPlanExercise()
                work_out_plan.name = name
                work_out_plan.trainer = trainer
                work_out_plan.plan = plan
                work_out_plan.save()
                messages.success(request, "Successfully Added Work Out Plan Exercise")
                return redirect(reverse('add_work_out_plan_exercise'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'admin_template/add_workout_plan_exercise_template.html', context)


def manage_trainer(request):
    trainers = CustomUser.objects.filter(user_type=2)
    context = {
        'trainers': trainers,
        'page_title': 'Manage Trainers'
    }
    return render(request, "admin_template/manage_trainer.html", context)


def manage_member(request):
    members = CustomUser.objects.filter(user_type=3)
    context = {
        'members': members,
        'page_title': 'Manage Members'
    }
    return render(request, "admin_template/manage_member.html", context)


def manage_work_out_plan(request):
    mwop = WorkoutPlan.objects.all()
    context = {
        'work_out_plan': mwop,
        'page_title': 'Manage Work Out Plan'
    }
    return render(request, "admin_template/manage_work_out_plan.html", context)


def manage_work_out_plan_exercise(request):
    mwope = WorkoutPlanExercise.objects.all()
    context = {
        'work_out_plan_exercise': mwope,
        'page_title': 'Manage Work Out Plan Exercise'
    }
    return render(request, "admin_template/manage_work_out_plan_exercise.html", context)


def edit_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    form = TrainerForm(request.POST or None, instance=trainer)
    context = {
        'form': form,
        'trainer_id': trainer_id,
        'page_title': 'Edit Trainer'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            work_out = form.cleaned_data.get('work_out')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=Trainer.trainer.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                trainer.work_out = work_out
                user.save()
                trainer.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_trainer', args=[trainer_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=trainer_id)
        trainer = Trainer.objects.get(id=user.id)
        return render(request, "admin_template/edit_trainer_template.html", context)


def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberForm(request.POST or None, instance=member)
    context = {
        'form': form,
        'member_id': member_id,
        'page_title': 'Edit Member'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            work_out = form.cleaned_data.get('work_out')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=Member.member.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                member.session = session
                user.gender = gender
                user.address = address
                member.work_out = work_out
                user.save()
                member.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_member', args=[member_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        user = CustomUser.objects.get(id=member_id)
        member = Member.objects.get(id=user.id)
        return render(request, "admin_template/edit_member_template.html", context)


def edit_work_out_plan(request, id):
    instance = get_object_or_404(WorkoutPlan, id=id)
    form = WorkoutPlanForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'id': id,
        'page_title': 'Edit Work Out Plan'
    }
    if request.method == 'POST':
        if form.is_valid():
            work_out = form.cleaned_data.get('work_out')
            try:
                wop = WorkoutPlan.objects.get(id=id)
                wop.work_out = work_out
                wop.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'admin_template/edit_work_out_plan_template.html', context)


def edit_work_out_plan_exercise(request, exercise_id):
    instance = get_object_or_404(WorkoutPlanExercise, id=exercise_id)
    form = WorkoutPlanExerciseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'exercise_id': exercise_id,
        'page_title': 'Edit Work Out Plan Exercise'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            plan = form.cleaned_data.get('plan')
            trainer = form.cleaned_data.get('trainer')
            try:
                wope = WorkoutPlanExercise.objects.get(id=exercise_id)
                wope.name = name
                wope.trainer = trainer
                wope.plan = plan
                wope.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_work_out_plan_exercise', args=[exercise_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'admin_template/edit_work_out_plan_exercise_template.html', context)


def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "admin_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "admin_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "admin_template/edit_session_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "admin_template/edit_session_template.html", context)

    else:
        return render(request, "admin_template/edit_session_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def member_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackMember.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Member Feedback Messages'
        }
        return render(request, 'admin_template/member_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackMember, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def trainer_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackTrainer.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Trainer Feedback Messages'
        }
        return render(request, 'admin_template/trainer_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackTrainer, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_trainer_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportTrainer.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Trainer'
        }
        return render(request, "admin_template/trainer_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportTrainer, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_member_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportMember.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Member'
        }
        return render(request, "admin_template/member_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportMember, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    wope = WorkoutPlanExercise.objects.all()
    sessions = Session.objects.all()
    context = {
        'work_out_plan_exercise': wope,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "admin_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    id = request.POST.get('work_out_plan')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        work_out_plan = get_object_or_404(WorkoutPlan, id=id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.member)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "admin_template/admin_view_profile.html", context)


def admin_notify_trainer(request):
    trainer = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Trainer",
        'allTrainer': trainer
    }
    return render(request, "admin_template/trainer_notification.html", context)


def admin_notify_member(request):
    member = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Member",
        'allMember': member
    }
    return render(request, "admin_template/member_notification.html", context)


@csrf_exempt
def send_member_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    member = get_object_or_404(Member, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Member Management System",
                'body': message,
                'click_action': reverse('member_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': Member.member.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationMember(member=member, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_trainer_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    trainer = get_object_or_404(Trainer, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Trainer Management System",
                'body': message,
                'click_action': reverse('trainer_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': trainer.trainer.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationTrainer(trainer=trainer, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(CustomUser, trainer__id=trainer_id)
    trainer.delete()
    messages.success(request, "Trainer deleted successfully!")
    return redirect(reverse('manage_trainer'))


def delete_member(request, member_id):
    member = get_object_or_404(CustomUser, member__id=member_id)
    member.delete()
    messages.success(request, "Member deleted successfully!")
    return redirect(reverse('manage_member'))


def delete_work_out_plan(request, id):
    wop = get_object_or_404(WorkoutPlan, id=id)
    try:
        wop.delete()
        messages.success(request, "Work Out Plan deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some members are assigned to this course already. Kindly change the affected member course and try again")
    return redirect(reverse('manage_work_out_plan'))


def delete_work_out_plan_exercise(request, exercise_id):
    wope = get_object_or_404(WorkoutPlanExercise, id=exercise_id)
    wope.delete()
    messages.success(request, "Work Out Plan Exercise deleted successfully!")
    return redirect(reverse('manage_work_out_plan_exercise'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are members assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))
