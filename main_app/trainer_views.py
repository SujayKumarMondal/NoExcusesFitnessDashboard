import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from . import forms, models
from datetime import date

def trainer_home(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    total_members = Member.objects.filter(work_out_plan=trainer.work_out_plan).count()
    total_leave = LeaveReportTrainer.objects.filter(trainer=trainer).count()
    wope = WorkoutPlanExercise.objects.filter(trainer=trainer)
    total_wope = wope.count()
    attendance_list = Attendance.objects.filter(subject__in=wope)
    total_attendance = attendance_list.count()
    attendance_list = []
    wope_list = []
    for w in wope:
        attendance_count = Attendance.objects.filter(w=w).count()
        wope_list.append(w.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'NoExcusesFitnes(Trainer Panel) - ' + str(trainer.trainer.first_name) + ' ' + str(trainer.trainer.last_name) + '' + ' (' + str(trainer.work_out_plan) + ')',
        'total_members': total_members,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_work_out_plan_exercise': total_wope,
        'work_out_plan_exercise_list': wope_list,
        'attendance_list': attendance_list
    }
    return render(request, 'trainer_template/home_content.html', context)


def trainer_take_attendance(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    wope = WorkoutPlanExercise.objects.filter(trainer_id=trainer)
    sessions = Session.objects.all()
    context = {
        'work_out_plan_exercises': wope,
        'sessions': sessions,
        'page_title': 'Take Member Attendance'
    }

    return render(request, 'trainer_template/staff_take_attendance.html', context)


@csrf_exempt
def get_members(request):
    exercise_id = request.POST.get('wope')
    session_id = request.POST.get('session')
    try:
        wope = get_object_or_404(WorkoutPlanExercise, id=exercise_id)
        session = get_object_or_404(Session, id=session_id)
        members = Member.objects.filter(
            work_out_id=wope.work_out_plan.id, session=session)
        member_data = []
        for mem in members:
            data = {
                    "id": mem.id,
                    "name": mem.member.first_name + " " + mem.member.last_name
                    }
            member_data.append(data)
        return JsonResponse(json.dumps(member_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def save_attendance(request):
    member_data = request.POST.get('c')
    date = request.POST.get('date')
    wope_id = request.POST.get('wope')
    session_id = request.POST.get('session')
    members = json.loads(member_data)
    try:
        session = get_object_or_404(Session, id=session_id)
        wope = get_object_or_404(WorkoutPlanExercise, id=wope_id)
        attendance = Attendance(session=session, subject=wope, date=date)
        attendance.save()

        for mem in members:
            member = get_object_or_404(Member, id=mem.get('id'))
            attendance_report = AttendanceReport(member=member, attendance=attendance, status=mem.get('status'))
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def trainer_update_attendance(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    wope = WorkoutPlanExercise.objects.filter(staff_id=trainer)
    sessions = Session.objects.all()
    context = {
        'work_out_plan_exercise': wope,
        'sessions': sessions,
        'page_title': 'Update Trainer Attendance'
    }

    return render(request, 'trainer_template/staff_update_attendance.html', context)


@csrf_exempt
def get_member_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        member_data = []
        for attendance in attendance_data:
            data = {"id": attendance.member.member.id,
                    "member": attendance.member.member.first_name + " " + attendance.member.member.last_name,
                    "status": attendance.status}
            member_data.append(data)
        return JsonResponse(json.dumps(member_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    member_data = request.POST.get('member_ids')
    date = request.POST.get('date')
    members = json.loads(member_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for mem in members:
            member = get_object_or_404(
                Member, admin_id=mem.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, member=member, attendance=attendance)
            attendance_report.status = mem.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def trainer_apply_leave(request):
    form = LeaveReportTrainerForm(request.POST or None)
    trainer = get_object_or_404(Trainer, admin_id=request.trainer.id)
    context = {
        'form': form,
        'leave_history': LeaveReportTrainer.objects.filter(staff=trainer),
        'page_title': 'Apply for Trainer Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.trainer = trainer
                obj.save()
                messages.success(
                    request, "Application for Trainer leave has been submitted for review")
                return redirect(reverse('trainer_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "trainer_template/staff_apply_leave.html", context)


def trainer_feedback(request):
    form = FeedbackTrainerForm(request.POST or None)
    trainer = get_object_or_404(Trainer, admin_id=request.trainer.id)
    context = {
        'form': form,
        'feedbacks': FeedbackTrainer.objects.filter(trainer=trainer),
        'page_title': 'Trainer Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.trainer = trainer
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('trainer_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "trainer_template/staff_feedback.html", context)


def trainer_view_profile(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    form = TrainerEditForm(request.POST or None, request.FILES or None,instance=trainer)
    context = {'form': form, 'page_title': 'View/Update Trainer Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                trainer = trainer.trainer
                if password != None:
                    trainer.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    trainer.profile_pic = passport_url
                trainer.first_name = first_name
                trainer.last_name = last_name
                trainer.address = address
                trainer.gender = gender
                trainer.save()
                trainer.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('trainer_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "trainer_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "trainer_template/staff_view_profile.html", context)

    return render(request, "trainer_template/staff_view_profile.html", context)


@csrf_exempt
def trainer_fcmtoken(request):
    token = request.POST.get('token')
    try:
        trainer_user = get_object_or_404(CustomUser, id=request.user.id)
        trainer_user.fcm_token = token
        trainer_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def trainer_view_notification(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    notifications = NotificationTrainer.objects.filter(staff=trainer)
    context = {
        'notifications': notifications,
        'page_title': "View Trainer Notifications"
    }
    return render(request, "trainer_template/staff_view_notification.html", context)


def trainer_add_result(request):
    trainer = get_object_or_404(Trainer, admin=request.trainer)
    wope = WorkoutPlanExercise.objects.filter(trainer=trainer)
    sessions = Session.objects.all()
    context = {
        'page_title': 'Member Result Upload',
        'subjects': wope,
        'sessions': sessions
    }
    if request.method == 'POST':
        try:
            member_id = request.POST.get('member_list')
            subject_id = request.POST.get('wope')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            member = get_object_or_404(Member, id=member_id)
            wope = get_object_or_404(WorkoutPlanExercise, id=subject_id)
            try:
                data = MemberResult.objects.get(
                    member=member, subject=wope)
                data.exam = exam
                data.test = test
                data.save()
                messages.success(request, "Scores Updated")
            except:
                result = MemberResult(member=member, subject=wope, test=test, exam=exam)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, "Error Occured While Processing Form")
    return render(request, "trainer_template/staff_add_result.html", context)


@csrf_exempt
def fetch_member_result(request):
    try:
        wope_id = request.POST.get('wope')
        member_id = request.POST.get('member')
        member = get_object_or_404(Member, id=member_id)
        wope = get_object_or_404(WorkoutPlanExercise, id=wope_id)
        result = MemberResult.objects.get(member=member, wope=wope)
        result_data = {
            'exam': result.exam,
            'test': result.test
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')

#library
def add_suppliment(request):
    if request.method == "POST":
        name = request.POST['name']
        brand = request.POST['brand']
        price = request.POST['price']
        category = request.POST['category']


        sup = Suppliments.objects.create(name=name, brand=brand, price=price, category=category )
        sup.save()
        alert = True
        return render(request, "trainer_template/add_book.html", {'alert':alert})
    context = {
        'page_title': "Add Suppliment"
    }
    return render(request, "trainer_template/add_book.html",context)

#issue book


def issue_suppliment(request):
    form = forms.IssueSupplimentsForm()
    if request.method == "POST":
        form = forms.IssueSupplimentsForm(request.POST)
        if form.is_valid():
            obj = models.IssuedSuppliments()
            obj.member_id = request.POST['name2']
            obj.price = request.POST['price']
            obj.save()
            alert = True
            return render(request, "trainer_template/issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "trainer_template/issue_book.html", {'form':form})

def view_issued_suppliment(request):
    issuedSuppliments = IssuedSuppliments.objects.all()
    details = []
    for i in issuedSuppliments:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        sup = list(models.Suppliments.objects.filter(price=i.price))
        # students = list(models.Student.objects.filter(admin=i.admin))
        i=0
        for l in sup:
            t=(sup[i].name,sup[i].price,issuedSuppliments[0].issued_date,issuedSuppliments[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "trainer_template/view_issued_book.html", {'issuedSuppliments':issuedSuppliments, 'details':details})