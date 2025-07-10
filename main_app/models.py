from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Trainer"), (3, "Member"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return  self.first_name + " " + self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class WorkoutPlan(models.Model):
    work_out = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.work_out

class Member(models.Model):
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    work_out = models.ForeignKey(WorkoutPlan, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.member.first_name + ", " + self.member.last_name
    
class Suppliments(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    price = models.CharField(max_length=13)
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + " ["+str(self.brand)+']'+ " ["+str(self.price)+']'

class SupplimentsStock(models.Model):
    member = models.ForeignKey(Member,  on_delete=models.CASCADE, null=True, blank=False)
    suppliments = models.ForeignKey(Suppliments,  on_delete=models.CASCADE, null=True, blank=False)
    def __str__(self):
        return str(self.member)

def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedSuppliments(models.Model):
    member_id = models.CharField(max_length=100, blank=True) 
    price = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)



class Trainer(models.Model):
    trainer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    work_out_plan = models.ForeignKey(WorkoutPlan, on_delete=models.DO_NOTHING, null=True, blank=False)

    def __str__(self):
        return self.trainer.first_name + " " +  self.trainer.last_name


class WorkoutPlanExercise(models.Model):
    name = models.CharField(max_length=120)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,)
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    work_out_plan = models.ForeignKey(WorkoutPlanExercise, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING, null=True, blank=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportTrainer(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackTrainer(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTrainer(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MemberResult(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    work_out_plan = models.ForeignKey(WorkoutPlanExercise, on_delete=models.CASCADE, null=True, blank=True)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Trainer.objects.create(admin=instance)
        if instance.user_type == 3:
            Member.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.trainer.save()
    if instance.user_type == 3:
        instance.member.save()

# todos
