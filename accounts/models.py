from django.db import models
from django.contrib.auth.models import User

import json

  
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    rate = models.FloatField(null=True,blank=True,default=0)
    rateCount = models.IntegerField(blank=True,null=True,default=0)
    serviceCount = models.IntegerField(blank=True,null=True,default=0)
    scheduleCount = models.IntegerField(blank=True,null=True,default=0)
    deliveryCount = models.IntegerField(blank=True,null=True,default=0)
    fiveStar = models.IntegerField(blank=True,null=True,default=0)
    birthday = models.DateField(null= True,blank=True)
    history = models.TextField(null =True, blank= True)
    notifications = models.TextField(null=True, blank=True)
    isRider = models.BooleanField(default=False)

    image = models.ImageField(upload_to='upload', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_history(self):
        return json.loads(self.history) if self.history else []

    def set_history(self, history_list):
        self.history = json.dumps(history_list)
    
    def get_notifications(self):
        return json.loads(self.notifications) if self.notifications else []

    def set_notifications(self, notification_list):
        self.notifications = json.dumps(notification_list)
        
    def increase_rating(self,rate):
        if int(rate)==5: self.fiveStar +=1
        
        if self.rateCount:
            temp = self.rate*self.rateCount
            self.rateCount+=1
            
            totalRate = temp+int(rate)
            self.rate = round(totalRate / self.rateCount, 2)
            
        else:
            self.rateCount=1
            self.rate = int(rate)
            
    def increase_service(self, schedule):
        if schedule.type_of_schedule in ['daily', 'weekly', 'monthly', 'custom']:
            self.scheduleCount += 1
        else:
            self.deliveryCount += 1

        self.serviceCount += 1

        
            
        


    
