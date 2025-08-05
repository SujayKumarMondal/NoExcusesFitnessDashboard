from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *
from . import models


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class EmployeeForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Employee
        fields = CustomUserForm.Meta.fields + \
            ['designation', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class HRForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HRForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = HR
        fields = CustomUserForm.Meta.fields + \
            ['designation' ]


class DesignationForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Designation


class ProjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['name', 'hr', 'designation']


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportHRForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportHRForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportHR
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackHRForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackHRForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackHR
        fields = ['feedback']


class LeaveReportEmployeeForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportEmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportEmployee
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackEmployeeForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackEmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackEmployee
        fields = ['feedback']


class EmployeeEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Employee
        fields = CustomUserForm.Meta.fields 


class HREditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HREditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = HR
        fields = CustomUserForm.Meta.fields


# class EditResultForm(FormSettings):
#     session_list = Session.objects.all()
#     session_year = forms.ModelChoiceField(
#         label="Session Year", queryset=session_list, required=True)

#     def __init__(self, *args, **kwargs):
#         super(EditResultForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = EmployeeResult
    #     fields = ['session_year', 'project', 'employee', 'test', 'exam']

#todos
# class TodoForm(forms.ModelForm):
#     class Meta:
#         model=Todo
#         fields=["title","is_finished"]

#issue asset

class IssueAssetForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Asset.objects.all(), empty_label="Asset Name [ISBN]", to_field_name="isbn", label="Asset (Name and ISBN)")
    name2 = forms.ModelChoiceField(queryset=models.Employee.objects.all(), empty_label="Name ", to_field_name="", label="Employee Details")
    
    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
