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


class MemberForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Member
        fields = CustomUserForm.Meta.fields + \
            ['work_out', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class TrainerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TrainerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Trainer
        fields = CustomUserForm.Meta.fields + \
            ['work_out_plan' ]


class WorkoutPlanForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(WorkoutPlanForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['work_out']
        model = WorkoutPlan


class WorkoutPlanExerciseForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(WorkoutPlanExerciseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WorkoutPlanExercise
        fields = ['name', 'trainer', 'plan']


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


class LeaveReportTrainerForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportTrainerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportTrainer
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackTrainerForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackTrainerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackTrainer
        fields = ['feedback']


class LeaveReportMemberForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportMemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportMember
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackMemberForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackMemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackMember
        fields = ['feedback']


class MemberEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(MemberEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Member
        fields = CustomUserForm.Meta.fields 


class TrainerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TrainerEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Trainer
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MemberResult
        fields = ['session_year', 'work_out_plan', 'member', 'test', 'exam']

#todos
# class TodoForm(forms.ModelForm):
#     class Meta:
#         model=Todo
#         fields=["title","is_finished"]

#issue book

class IssueSupplimentsForm(forms.Form):
    price2 = forms.ModelChoiceField(queryset=models.Suppliments.objects.all(), empty_label="Suppliment Name [Price]", to_field_name="price", label="Suppliment (Name and Price)")
    name2 = forms.ModelChoiceField(queryset=models.Member.objects.all(), empty_label="Name ", to_field_name="", label="Member Details")
    
    price2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
