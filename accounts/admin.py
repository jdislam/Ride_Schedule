from django.contrib import admin
from accounts.models import Profile
from schedules.models import Schedule
# Register your models here.
admin.site.register([Profile,Schedule])
