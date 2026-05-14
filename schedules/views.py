
from schedules.models import Schedule
from django.contrib.auth.models import User, auth
from datetime import date
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render ,redirect
from accounts.models import Profile
from schedules.models import Schedule

from .scheduleForm import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from schedules.decorators import rider_required , driver_required

# Create your views here.

@rider_required(redirect_url='home')
def weeklySchedule(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        week=''
        if(request.POST.get('SUN')): week = week+request.POST.get('SUN')
        if(request.POST.get('MON')): week = week+' '+request.POST.get('MON')
        if(request.POST.get('TUE')): week = week+' '+request.POST.get('TUE')
        if(request.POST.get('WED')): week = week+' '+request.POST.get('WED')
        if(request.POST.get('THE')): week = week+' '+request.POST.get('THE')
        if(request.POST.get('FRI')): week = week+' '+request.POST.get('FRI')
        if(request.POST.get('SAT')): week = week+' '+request.POST.get('SAT')

        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='weekly',price=price,startDate=startDate,endDate=endDate,weeks=week)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)

    return render(request,'schedule/weeklySchedule.html')

@rider_required(redirect_url='home')
def monthlySchedule(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        week=''
        if(request.POST.get('SUN')): week = week+request.POST.get('SUN')
        if(request.POST.get('MON')): week = week+' '+request.POST.get('MON')
        if(request.POST.get('TUE')): week = week+' '+request.POST.get('TUE')
        if(request.POST.get('WED')): week = week+' '+request.POST.get('WED')
        if(request.POST.get('THE')): week = week+' '+request.POST.get('THE')
        if(request.POST.get('FRI')): week = week+' '+request.POST.get('FRI')
        if(request.POST.get('SAT')): week = week+' '+request.POST.get('SAT')

        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='monthly',price=price,startDate=startDate,endDate=endDate,weeks=week)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)


    return render(request,'schedule/monthlySchedule.html')

@rider_required(redirect_url='home')
def dailySchedule(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        # endDate = request.POST.get('endDate')

        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='daily',price=price,startDate=startDate)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)


    return render(request,'schedule/dailySchedule.html')


@driver_required(redirect_url='home')
def schedulePost(request):
    
    schedulePost = Schedule.objects.all().order_by("pickUp_time")

    posts = {
        'schedulePost': schedulePost,
        
    }
    return render(request, template_name='schedule/schedulePost.html', context=posts)

@login_required(login_url='login')
def userPost(request):
    
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
           
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    } 
    return render(request, 'accounts/userPost.html', context)


@driver_required(redirect_url='home')
def takeSchedule(request , id):
    schedule= Schedule.objects.get(pk = id)
    
    context={
        'title':'Take Schedule',
        'm2':'Do you want to take this schedule?',
        'text1': 'From: '+schedule.pickup_from +'\n To: '+schedule.drop_to,
        'text2': 'Price: '+str(schedule.price)+'TK',
        'url':'schedulePost',
    }
    if request.method == 'POST':
        schedule.pending = False
        schedule.driver_id = request.user.username
        createHistory(request,schedule,"accepted")
        createNotification(request,schedule,"accepted")
        schedule.save()
        
        return redirect('schedulePost')
    return render(request, 'notification/confirm.html',context)


@login_required(login_url='login')
def deleteSchedule(request , id):
    schedule = Schedule.objects.get(pk = id)
    context={
        'title':'Delete Schedule',
        'm1':'are your sure?',
        'url':'userPost',
    }
    if request.method == 'POST':
        createHistory(request,schedule,"canceled")
        createNotification(request,schedule,"canceled")
        schedule.delete()
        return redirect('userPost')
    return render(request, 'notification/confirm.html',context)

@login_required(login_url='login')
def completeSchedule(request , id):
    schedule = Schedule.objects.get(pk = id)
    context={
        'title':str(schedule.type_of_schedule) + ' Completed',
        'm1':'Do you want to Rate '+ str(schedule.driver_id) + '?',
        'text1': schedule.driver_id,
        'schedule':id,
        'url1':'rateDriver',
        'url2':'userPost',
    }
    if request.method == 'POST':
        
        rider = request.user.profile
        user = User.objects.get(username = schedule.driver_id)
        driver = Profile.objects.get(user = user)
        
        rider.increase_service(schedule)
        rider.save()
        driver.increase_service(schedule)
        driver.save()
        createHistory(request,schedule,"completed")
        schedule.delete()
        return redirect('userPost')
    return render(request, 'notification/completeService.html',context)




@login_required(login_url='login')
def updateSchedule(request, id):
    try:
        schedule = Schedule.objects.get(pk = id)
        form = ScheduleForm(instance=schedule)
    
        if request.method == 'POST':
            form = ScheduleForm(request.POST, request.FILES, instance=schedule)
            if form.is_valid():
                form.save()
                context = { 
                'title':'Successfull',
                'm1': request.user.username,
                'm2':'your schedule Update Successfull',
                'url':'userPost',
                }
                createHistory(request,schedule,"updated")
                return render(request , 'notification/message.html' , context)
        return render(request, 'update/updateSchedule.html',{'form': form })
    except:
        return render(request, 'update/updateSchedule.html')
    
    
def allService(request):
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
    return render (request,'schedule/allservice.html',context)


@rider_required(redirect_url='home')
def parcelDelivery(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        weight = request.POST.get('Sweight')

        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='Parcel Delivery',price=price,startDate=startDate,weight=weight)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'Parcel Delivery schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)


    return render(request,'delivery/parcel.html')

@rider_required(redirect_url='home')
def courier(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        weight = request.POST.get('Sweight')
        phone = request.POST.get('Sphone')
 
        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='Courier',price=price,startDate=startDate,weight=weight,phone=phone)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'Courier schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)


    return render(request,'delivery/courier.html')


@rider_required(redirect_url='home')
def pharmacy(request):
    if request.method == 'POST':
        rider = request.user.profile
        pickUp_time = request.POST.get('startTime')
        pickUp_from = request.POST.get('picklocation')
        drop_to = request.POST.get('droplocation')
        price = request.POST.get('SPrice')
        startDate = request.POST.get('startDate')
        weight = request.POST.get('Sweight')
        phone = request.POST.get('Sphone')
 
        schedule = Schedule.objects.create(rider_id=rider,pickUp_time=pickUp_time,pickup_from=pickUp_from,drop_to=drop_to,type_of_schedule='Pharmacy',price=price,startDate=startDate,weight=weight,phone=phone)
        createHistory(request,schedule,"created")
        schedule.save()
        context = { 
            'title':'Successfull',
            'm1': 'Pharmacy schedule created successfull',
            'url':'home',
            }
        return render(request , 'notification/message.html' , context)


    return render(request,'delivery/pharmacy.html')


def createNotification(request,schedule,status):
    
    user = User.objects.get(username = schedule.rider_id) 

    profile = Profile.objects.get(user=user)
    
    data = {
        "id": str(datetime.now().isoformat()),
        "time": str(date.today()),  
        "driver": str(schedule.driver_id),
        "rider": str(schedule.rider_id),
        "date": str(schedule.startDate)+" - "+str(schedule.endDate),
        "pickUp":str(schedule.pickUp_time), 
        "type":str(schedule.type_of_schedule) ,
        "location": str(schedule.pickup_from)+" - "+str(schedule.drop_to),
        "price":str(schedule.price),
        "status": status
    }
    notification = profile.get_notifications()
    notification.append(data)
    
    if len(notification) > 10:
        notification = notification[-10:]
        
    profile.set_notifications(notification)
    profile.save()
    
    

def createHistory(request, schedule, status):
    user1 = User.objects.get(username = schedule.rider_id) 

    profile1 = Profile.objects.get(user=user1)
    history1 = profile1.get_history()
    

    
    
    history = {
        "id": str(datetime.now().isoformat()),
        "time": str(date.today()),  
        "driver": str(schedule.driver_id),
        "rider": str(schedule.rider_id),
        "date": str(schedule.startDate)+" - "+str(schedule.endDate),
        "pickUp":str(schedule.pickUp_time), 
        "type":str(schedule.type_of_schedule) ,
        "location": str(schedule.pickup_from)+" - "+str(schedule.drop_to),
        "price":str(schedule.price),
        "status": status
    }
    if schedule.driver_id is not None and schedule.driver_id.strip() != "":
        user2 = User.objects.get(username = schedule.driver_id)
        profile2 = Profile.objects.get(user = user2)
        history2 = profile2.get_history()
        history2.append(history)
        profile2.set_history(history2)
        profile2.save()
        
    history1.append(history)     
    profile1.set_history(history1)
    profile1.save()
    
    
    
    
def readHistory(request):
    
    try:
        profile = request.user.profile
        notification = profile.get_notifications()
        history = profile.get_history()
        history = history[::-1]
        if request.user.profile.isRider:
            schedule = Schedule.objects.filter(rider_id=request.user.profile).order_by("pickUp_time")
        else:
            schedule = Schedule.objects.filter(driver_id=request.user.username).order_by("pickUp_time")
        
    except Exception as e:
        
        notification = []
        history = []
        schedule = []
           
    context = {
        'notification':notification,
        'history':history,
        'schedule':schedule
    } 
    return render(request, 'accounts/userHistory.html', context)



def deleteHistory(request,id):
         
    profile = request.user.profile
    history = profile.get_history()

    history = [item for item in history if item.get('id') != id]

    profile.set_history(history)
    profile.save()

    return redirect('readHistory')  

def deleteAllHistory(request):
    profile = request.user.profile
    profile.set_history([])  
    profile.save()           
    return redirect('readHistory')

def deleteAllNotification(request):
    profile = request.user.profile
    profile.set_notifications([])  
    profile.save()           
    return redirect('/')


