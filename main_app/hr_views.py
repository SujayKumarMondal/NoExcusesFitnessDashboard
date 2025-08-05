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

def hr_home(request):
    hr = get_object_or_404(HR, admin=request.user)
    total_employees = Employee.objects.filter(designation=hr.designation).count()
    total_leave = LeaveReportHR.objects.filter(hr=hr).count()
    projects = Project.objects.filter(hr=hr)
    total_project = projects.count()
    attendance_list = Attendance.objects.filter(project__in=projects)
    total_attendance = attendance_list.count()
    attendance_list = []
    project_list = []
    for project in projects:
        attendance_count = Attendance.objects.filter(project=project).count()
        project_list.append(project.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'TeamOps(HR Panel) - ' + str(hr.admin.first_name) + ' ' + str(hr.admin.last_name) + '' + ' (' + str(hr.designation) + ')',
        'total_employees': total_employees,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_project': total_project,
        'project_list': project_list,
        'attendance_list': attendance_list
    }
    return render(request, 'hr_template/home_content.html', context)


def hr_take_attendance(request):
    hr = get_object_or_404(HR, admin=request.user)
    projects = Project.objects.filter(hr_id=hr)
    sessions = Session.objects.all()
    context = {
        'projects': projects,
        'sessions': sessions,
        'page_title': 'Take Attendance'
    }

    return render(request, 'hr_template/hr_take_attendance.html', context)


@csrf_exempt
def get_employees(request):
    project_id = request.POST.get('project')
    session_id = request.POST.get('session')
    try:
        project = get_object_or_404(Project, id=project_id)
        session = get_object_or_404(Session, id=session_id)
        employees = Employee.objects.filter(
            designation_id=project.designation.id, session=session)
        employee_data = []
        for employee in employees:
            data = {
                    "id": employee.id,
                    "name": employee.admin.first_name + " " + employee.admin.last_name
                    }
            employee_data.append(data)
        return JsonResponse(json.dumps(employee_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def save_attendance(request):
    employee_data = request.POST.get('employee_ids')
    date = request.POST.get('date')
    project_id = request.POST.get('project')
    session_id = request.POST.get('session')
    employees = json.loads(employee_data)
    try:
        session = get_object_or_404(Session, id=session_id)
        project = get_object_or_404(Project, id=project_id)
        attendance = Attendance(session=session, project=project, date=date)
        attendance.save()

        for employee_dict in employees:
            employee = get_object_or_404(Employee, id=employee_dict.get('id'))
            attendance_report = AttendanceReport(employee=employee, attendance=attendance, status=employee_dict.get('status'))
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def hr_update_attendance(request):
    hr = get_object_or_404(HR, admin=request.user)
    projects = Project.objects.filter(hr_id=hr)
    sessions = Session.objects.all()
    context = {
        'projects': projects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request, 'hr_template/hr_update_attendance.html', context)


@csrf_exempt
def get_employee_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        employee_data = []
        for attendance in attendance_data:
            data = {"id": attendance.employee.admin.id,
                    "name": attendance.employee.admin.last_name + " " + attendance.employee.admin.first_name,
                    "status": attendance.status}
            employee_data.append(data)
        return JsonResponse(json.dumps(employee_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    employee_data = request.POST.get('employee_ids')
    date = request.POST.get('date')
    employees = json.loads(employee_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for employee_dict in employees:
            employee = get_object_or_404(
                Employee, admin_id=employee_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, employee=employee, attendance=attendance)
            attendance_report.status = employee_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def hr_apply_leave(request):
    form = LeaveReportHRForm(request.POST or None)
    hr = get_object_or_404(HR, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportHR.objects.filter(hr=hr),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.hr = hr
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('hr_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "hr_template/hr_apply_leave.html", context)


def hr_feedback(request):
    form = FeedbackHRForm(request.POST or None)
    hr = get_object_or_404(HR, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackHR.objects.filter(hr=hr),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.hr = hr
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('hr_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "hr_template/hr_feedback.html", context)


def hr_view_profile(request):
    hr = get_object_or_404(HR, admin=request.user)
    form = HREditForm(request.POST or None, request.FILES or None,instance=hr)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = hr.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                hr.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('hr_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "hr_template/hr_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "hr_template/hr_view_profile.html", context)

    return render(request, "hr_template/hr_view_profile.html", context)


@csrf_exempt
def hr_fcmtoken(request):
    token = request.POST.get('token')
    try:
        hr_user = get_object_or_404(CustomUser, id=request.user.id)
        hr_user.fcm_token = token
        hr_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def hr_view_notification(request):
    hr = get_object_or_404(HR, admin=request.user)
    notifications = NotificationHR.objects.filter(hr=hr)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "hr_template/hr_view_notification.html", context)


# def hr_add_result(request):
#     hr = get_object_or_404(HR, admin=request.user)
#     projects = Project.objects.filter(hr=hr)
#     sessions = Session.objects.all()
#     context = {
#         'page_title': 'Result Upload',
#         'projects': projects,
#         'sessions': sessions
#     }
#     if request.method == 'POST':
#         try:
#             employee_id = request.POST.get('employee_list')
#             project_id = request.POST.get('project')
#             test = request.POST.get('test')
#             exam = request.POST.get('exam')
#             employee = get_object_or_404(Employee, id=employee_id)
#             project = get_object_or_404(Project, id=project_id)
#             try:
#                 data = EmployeeResult.objects.get(
#                     employee=employee, project=project)
#                 data.exam = exam
#                 data.test = test
#                 data.save()
#                 messages.success(request, "Scores Updated")
#             except:
#                 result = EmployeeResult(employee=employee, project=project, test=test, exam=exam)
#                 result.save()
#                 messages.success(request, "Scores Saved")
#         except Exception as e:
#             messages.warning(request, "Error Occured While Processing Form")
#     return render(request, "hr_template/hr_add_result.html", context)


# @csrf_exempt
# def fetch_employee_result(request):
#     try:
#         project_id = request.POST.get('project')
#         employee_id = request.POST.get('employee')
#         employee = get_object_or_404(Employee, id=employee_id)
#         project = get_object_or_404(Project, id=project_id)
#         result = EmployeeResult.objects.get(employee=employee, project=project)
#         result_data = {
#             'exam': result.exam,
#             'test': result.test
#         }
#         return HttpResponse(json.dumps(result_data))
#     except Exception as e:
#         return HttpResponse('False')

#store
def add_asset(request):
    if request.method == "POST":
        name = request.POST['name']
        brand = request.POST['brand']
        isbn = request.POST['isbn']
        category = request.POST['category']


        assets = Asset.objects.create(name=name, brand=brand, isbn=isbn, category=category )
        assets.save()
        alert = True
        return render(request, "hr_template/add_asset.html", {'alert':alert})
    context = {
        'page_title': "Add Asset"
    }
    return render(request, "hr_template/add_asset.html",context)

#issue asset


def issue_asset(request):
    form = forms.IssueAssetForm()
    if request.method == "POST":
        form = forms.IssueAssetForm(request.POST)
        if form.is_valid():
            obj = models.IssuedAsset()
            obj.employee_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "hr_template/issue_asset.html", {'obj':obj, 'alert':alert})
    return render(request, "hr_template/issue_asset.html", {'form':form})

def view_issued_asset(request):
    issuedAssets = IssuedAsset.objects.all()
    details = []
    for i in issuedAssets:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        assets = list(models.Asset.objects.filter(isbn=i.isbn))
        i=0
        for l in assets:
            t=(assets[i].name,assets[i].isbn,issuedAssets[0].issued_date,issuedAssets[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "hr_template/view_issued_asset.html", {'issuedAssets':issuedAssets, 'details':details})