import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def member_home(request):
    member = get_object_or_404(Member, member=request.member)
    total_work_out_plan_exercise = WorkoutPlanExercise.objects.filter(plan=member.plan).count()
    total_attendance = AttendanceReport.objects.filter(member=member).count()
    total_present = AttendanceReport.objects.filter(member=member, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    work_out_plan_exercise_name = []
    data_present = []
    data_absent = []
    wope = WorkoutPlanExercise.objects.filter(course=member.course)
    for w in wope:
        attendance = Attendance.objects.filter(w=w)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, member=member).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, member=member).count()
        work_out_plan_exercise_name.append(w.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_work_out_plan_exercise': total_work_out_plan_exercise,
        'wope': wope,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': work_out_plan_exercise_name,
        'page_title': '(NoExcusesFitness(Member Panel) - ' + str(member.member.first_name) + ' ' + str(member.member.last_name)

    }
    return render(request, 'member_template/home_content.html', context)


@ csrf_exempt
def member_view_attendance(request):
    member = get_object_or_404(Member, member=request.member)
    if request.method != 'POST':
        work_out = get_object_or_404(WorkoutPlan, id=member.work_out.id)
        context = {
            'wope': WorkoutPlanExercise.objects.filter(work_out=work_out),
            'page_title': 'View Member Attendance'
        }
        return render(request, 'member_template/student_view_attendance.html', context)
    else:
        exercise_id = request.POST.get('wope')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            wope = get_object_or_404(WorkoutPlanExercise, exercise_id=exercise_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), wope=wope)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, member=member)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def member_apply_leave(request):
    form = LeaveReportMemberForm(request.POST or None)
    member = get_object_or_404(Member, admin_id=request.member.id)
    context = {
        'form': form,
        'leave_history': LeaveReportMember.objects.filter(member=member),
        'page_title': 'Apply for Member leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.member = member
                obj.save()
                messages.success(
                    request, "Application for Member leave has been submitted for review")
                return redirect(reverse('member_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "member_template/student_apply_leave.html", context)


def member_feedback(request):
    form = FeedbackMemberForm(request.POST or None)
    member = get_object_or_404(Member, admin_id=request.member.id)
    context = {
        'form': form,
        'feedbacks': FeedbackMember.objects.filter(member=member),
        'page_title': 'Member Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.member = member
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('member_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "member_template/student_feedback.html", context)


def member_view_profile(request):
    member = get_object_or_404(Member, admin=request.member)
    form = MemberEditForm(request.POST or None, request.FILES or None,
                           instance=member)
    context = {'form': form,
               'page_title': 'View/Edit Member Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                member = member.member
                if password != None:
                    member.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    member.profile_pic = passport_url
                member.first_name = first_name
                member.last_name = last_name
                member.address = address
                member.gender = gender
                member.save()
                member.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('member_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "member_template/student_view_profile.html", context)


@csrf_exempt
def member_fcmtoken(request):
    token = request.POST.get('token')
    member_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        member_user.fcm_token = token
        member_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def member_view_notification(request):
    member = get_object_or_404(Member, admin=request.member)
    notifications = NotificationMember.objects.filter(member=member)
    context = {
        'notifications': notifications,
        'page_title': "View Member Notifications"
    }
    return render(request, "member_template/student_view_notification.html", context)


def member_view_result(request):
    member = get_object_or_404(Member, admin=request.member)
    results = MemberResult.objects.filter(member=member)
    context = {
        'results': results,
        'page_title': "View Member Results"
    }
    return render(request, "member_template/student_view_result.html", context)


#library

def view_suppliments(request):
    sup = Suppliments.objects.all()
    context = {
        'suppliments': sup,
        'page_title': "SupplimentsStock"
    }
    return render(request, "member_template/view_books.html", context)

