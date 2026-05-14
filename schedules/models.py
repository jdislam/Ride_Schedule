from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your models here.
class Schedule(models.Model):
    rider_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    driver_id = models.CharField(blank=True,null=True,max_length=20)
    
    pickUp_time = models.CharField(max_length=10)
    pickup_from = models.CharField(max_length=50)
    drop_to = models.CharField(max_length=50)
    pending = models.BooleanField(default=True)
    schedule_type = (
        ('daily','daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('Parcel Delivery', 'Parcel Delivery'),
        ('Courier', 'Courier'),
        ('Pharmacy', 'Pharmacy'),
        ('custom', 'custom'))
    type_of_schedule = models.CharField(max_length=20,choices=schedule_type,blank=True,null=True)
    price = models.IntegerField(blank=True, null=True)
    startDate = models.DateField(blank=True,null=True)
    endDate = models.DateField(blank=True,null=True)
    weeks = models.CharField(max_length=30,blank=True,null=True)
    weight = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=14,blank=True,null=True)


    def __str__(self):
        return self.pickUp_time

