from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(HR)
admin.site.register(Employee)
admin.site.register(Designation)
admin.site.register(Asset)
admin.site.register(IssuedAsset)
admin.site.register(Store)
admin.site.register(Project)
admin.site.register(Session)

