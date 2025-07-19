from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import Project, HR, Employee, EmployeeResult
from .forms import EditResultForm
from django.urls import reverse


class EditResultView(View):
    def get(self, request, *args, **kwargs):
        resultForm = EditResultForm()
        hr = get_object_or_404(HR, admin=request.user)
        resultForm.fields['project'].queryset = Project.objects.filter(hr=hr)
        context = {
            'form': resultForm,
            'page_title': "Edit Employee's Result"
        }
        return render(request, "hr_template/edit_employee_result.html", context)

    def post(self, request, *args, **kwargs):
        form = EditResultForm(request.POST)
        context = {'form': form, 'page_title': "Edit Employee's Result"}
        if form.is_valid():
            try:
                employee = form.cleaned_data.get('employee')
                project = form.cleaned_data.get('project')
                test = form.cleaned_data.get('test')
                exam = form.cleaned_data.get('exam')
                # Validating
                result = EmployeeResult.objects.get(employee=employee, project=project)
                result.exam = exam
                result.test = test
                result.save()
                messages.success(request, "Result Updated")
                return redirect(reverse('edit_employee_result'))
            except Exception as e:
                messages.warning(request, "Result Could Not Be Updated")
        else:
            messages.warning(request, "Result Could Not Be Updated")
        return render(request, "hr_template/edit_employee_result.html", context)
