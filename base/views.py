from django.shortcuts import render
from accounts.models import Profile
from django.contrib.auth.models import User, auth
from schedules.models import Schedule

# Create your views here.
def home(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
      
    notification = notification[::-1]      
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    }
    
    return render (request, 'pages/home.html',context)


def help(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
     
    notification = notification[::-1]       
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    }
    
    return render(request, 'pages/help.html',context)


def contact(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
    
    notification = notification[::-1]        
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    }
    
    return render(request, 'pages/contact.html',context)

def rateUs(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
    
    notification = notification[::-1]        
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    }
    return render(request, 'pages/rateUs.html',context)

def policy(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
    
    notification = notification[::-1]       
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    } 
    return render(request , 'pages/policy.html',context)


def helpToJoin(request):
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
    
    notification = notification[::-1]       
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    } 
    return render(request , 'pages/joinPage.html',context)
