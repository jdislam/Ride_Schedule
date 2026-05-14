from django.forms import ModelForm
from .models import *

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['pickUp_time','pickup_from','drop_to','type_of_schedule','price','startDate','endDate','weeks']