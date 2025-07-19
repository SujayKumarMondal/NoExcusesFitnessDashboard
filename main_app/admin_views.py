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


def admin_home(request):
    total_hr = HR.objects.all().count()
    total_employees = Employee.objects.all().count()
    projects = Project.objects.all()
    total_project = projects.count()
    total_designation = Designation.objects.all().count()
    attendance_list = Attendance.objects.filter(project__in=projects)
    total_attendance = attendance_list.count()
    attendance_list = []
    project_list = []
    for project in projects:
        attendance_count = Attendance.objects.filter(project=project).count()
        project_list.append(project.name[:7])
        attendance_list.append(attendance_count)

    # Total projects and employees in Each designation
    designation_all = Designation.objects.all()
    designation_name_list = []
    project_count_list = []
    employee_count_list_in_designation = []

    for designation in designation_all:
        projects = Project.objects.filter(designation_id=designation.id).count()
        employees = Employee.objects.filter(designation_id=designation.id).count()
        designation_name_list.append(designation.name)
        project_count_list.append(projects)
        employee_count_list_in_designation.append(employees)
    
    project_all = Project.objects.all()
    project_list = []
    employee_count_list_in_project = []
    for project in project_all:
        designation = Designation.objects.get(id=project.designation.id)
        employee_count = Employee.objects.filter(designation_id=designation.id).count()
        project_list.append(project.name)
        employee_count_list_in_project.append(employee_count)


    # For Employees
    employee_attendance_present_list=[]
    employee_attendance_leave_list=[]
    employee_name_list=[]

    employees = Employee.objects.all()
    for employee in employees:
        
        attendance = AttendanceReport.objects.filter(employee_id=employee.id, status=True).count()
        absent = AttendanceReport.objects.filter(employee_id=employee.id, status=False).count()
        leave = LeaveReportEmployee.objects.filter(employee_id=employee.id, status=1).count()
        employee_attendance_present_list.append(attendance)
        employee_attendance_leave_list.append(leave+absent)
        employee_name_list.append(employee.admin.first_name)

    context = {
        'page_title': "TeamOps(Administrative Dashboard)",
        'total_employees': total_employees,
        'total_hr': total_hr,
        'total_designation': total_designation,
        'total_project': total_project,
        'project_list': project_list,
        'attendance_list': attendance_list,
        'employee_attendance_present_list': employee_attendance_present_list,
        'employee_attendance_leave_list': employee_attendance_leave_list,
        "employee_name_list": employee_name_list,
        "employee_count_list_in_project": employee_count_list_in_project,
        "employee_count_list_in_designation": employee_count_list_in_designation,
        "designation_name_list": designation_name_list,

    }
    return render(request, 'admin_template/home_content.html', context)


def add_hr(request):
    form = HRForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add HR'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            designation = form.cleaned_data.get('designation')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.hr.designation = designation
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_hr'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'admin_template/add_hr_template.html', context)


def add_employee(request):
    employee_form = EmployeeForm(request.POST or None, request.FILES or None)
    context = {'form': employee_form, 'page_title': 'Add Employee'}
    if request.method == 'POST':
        if employee_form.is_valid():
            first_name = employee_form.cleaned_data.get('first_name')
            last_name = employee_form.cleaned_data.get('last_name')
            address = employee_form.cleaned_data.get('address')
            email = employee_form.cleaned_data.get('email')
            gender = employee_form.cleaned_data.get('gender')
            password = employee_form.cleaned_data.get('password')
            designation = employee_form.cleaned_data.get('designation')
            session = employee_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.employee.session = session
                user.employee.designation = designation
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_employee'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'admin_template/add_employee_template.html', context)


def add_designation(request):
    form = DesignationForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Designation'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                designation = Designation()
                designation.name = name
                designation.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_designation'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin_template/add_designation_template.html', context)


def add_project(request):
    form = ProjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add project'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            designation = form.cleaned_data.get('designation')
            hr = form.cleaned_data.get('hr')
            try:
                project = Project()
                project.name = name
                project.hr = hr
                project.designation = designation
                project.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_project'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'admin_template/add_project_template.html', context)


def manage_hr(request):
    allHR = CustomUser.objects.filter(user_type=2)
    context = {
        'allHR': allHR,
        'page_title': 'Manage HR'
    }
    return render(request, "admin_template/manage_hr.html", context)


def manage_employee(request):
    employees = CustomUser.objects.filter(user_type=3)
    context = {
        'employees': employees,
        'page_title': 'Manage Employees'
    }
    return render(request, "admin_template/manage_employee.html", context)


def manage_designation(request):
    designations = Designation.objects.all()
    context = {
        'designations': designations,
        'page_title': 'Manage designations'
    }
    return render(request, "admin_template/manage_designation.html", context)


def manage_project(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'page_title': 'Manage projects'
    }
    return render(request, "admin_template/manage_project.html", context)


def edit_hr(request, hr_id):
    hr = get_object_or_404(HR, id=hr_id)
    form = HRForm(request.POST or None, instance=hr)
    context = {
        'form': form,
        'hr_id': hr_id,
        'page_title': 'Edit HR'
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
            designation = form.cleaned_data.get('designation')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=hr.admin.id)
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
                hr.designation = designation
                user.save()
                hr.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_hr', args=[hr_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=hr_id)
        hr = HR.objects.get(id=user.id)
        return render(request, "admin_template/edit_hr_template.html", context)


def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    form = EmployeeForm(request.POST or None, instance=employee)
    context = {
        'form': form,
        'employee_id': employee_id,
        'page_title': 'Edit Employee'
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
            designation = form.cleaned_data.get('designation')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=employee.admin.id)
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
                employee.session = session
                user.gender = gender
                user.address = address
                employee.designation = designation
                user.save()
                employee.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_employee', args=[employee_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin_template/edit_employee_template.html", context)


def edit_designation(request, designation_id):
    instance = get_object_or_404(Designation, id=designation_id)
    form = DesignationForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'designation_id': designation_id,
        'page_title': 'Edit designation'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                designation = Designation.objects.get(id=designation_id)
                designation.name = name
                designation.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'admin_template/edit_designation_template.html', context)


def edit_project(request, project_id):
    instance = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'project_id': project_id,
        'page_title': 'Edit project'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            designation = form.cleaned_data.get('designation')
            hr = form.cleaned_data.get('hr')
            try:
                project = Project.objects.get(id=project_id)
                project.name = name
                project.hr = hr
                project.designation = designation
                project.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_project', args=[project_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'admin_template/edit_project_template.html', context)


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
def employee_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackEmployee.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Employee Feedback Messages'
        }
        return render(request, 'admin_template/employee_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackEmployee, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def hr_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackHR.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'HR Feedback Messages'
        }
        return render(request, 'admin_template/hr_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackHR, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_hr_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportHR.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From HR'
        }
        return render(request, "admin_template/hr_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportHR, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_employee_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportEmployee.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Employees'
        }
        return render(request, "admin_template/employee_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportEmployee, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    projects = Project.objects.all()
    sessions = Session.objects.all()
    context = {
        'projects': projects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "admin_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    project_id = request.POST.get('project')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        project = get_object_or_404(Project, id=project_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.employee)
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


def admin_notify_hr(request):
    hr = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To HR",
        'allHR': hr
    }
    return render(request, "admin_template/hr_notification.html", context)


def admin_notify_employee(request):
    employee = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Employees",
        'employees': employee
    }
    return render(request, "admin_template/employee_notification.html", context)


@csrf_exempt
def send_employee_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    employee = get_object_or_404(Employee, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Employee Management System",
                'body': message,
                'click_action': reverse('employee_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': employee.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationEmployee(employee=employee, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_hr_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    hr = get_object_or_404(HR, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Employee Management System",
                'body': message,
                'click_action': reverse('hr_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': hr.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationHR(hr=hr, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_hr(request, hr_id):
    hr = get_object_or_404(CustomUser, hr__id=hr_id)
    hr.delete()
    messages.success(request, "HR deleted successfully!")
    return redirect(reverse('manage_hr'))


def delete_employee(request, employee_id):
    employee = get_object_or_404(CustomUser, employee__id=employee_id)
    employee.delete()
    messages.success(request, "employee deleted successfully!")
    return redirect(reverse('manage_employee'))


def delete_designation(request, designation_id):
    designation = get_object_or_404(Designation, id=designation_id)
    try:
        designation.delete()
        messages.success(request, "designation deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some employees are assigned to this designation already. Kindly change the affected employee designation and try again")
    return redirect(reverse('manage_designation'))


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect(reverse('manage_project'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are employees assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))
