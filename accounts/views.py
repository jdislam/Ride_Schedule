from django.shortcuts import render
from django.shortcuts import render ,redirect
from accounts.models import Profile
from schedules.models import Schedule

from .forms import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.


@login_required(login_url='login')
def userProfile(request):
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
    return render(request,'accounts/userProfile.html',context)


def createRider(request):
    if request.method == 'POST':
        is_rider = request.POST.get('isRider')
        username = request.POST.get('usernameSignUp')
        email = request.POST.get('emailSignUp')
        password = request.POST.get('passwordSignUp')
        cpassword = request.POST.get('cpasswordSignUp')
        print("this is Rider")
        print(is_rider)
        if (password==cpassword and uniqueUserName(username) and len(password) > 3 and len(email)>10):
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            is_rider_bool = is_rider == "True"
            
            profile = Profile.objects.create(user=user, isRider=is_rider_bool,rate = 0, rateCount = 0,serviceCount = 0,scheduleCount = 0,deliveryCount = 0,fiveStar = 0)
            profile.save()
            context = { 
                    'title':'Welcome',
                    'm1': username,
                    'm2':'your Driver account created successfully',
                    'm3':'Make sure to remember your username or password to Login',
                    'url':'home',
                }
            login(request,user)
            return render(request , 'notification/message.html' , context)
            
        else:
            
            context = { 
                    'title':'Fail!',
                    'm1' : 'Account already exists with this Username! or Confirm Password is wrong',
                    'm2': 'Try again',
                    'url':'home',
                }
            return render(request , 'notification/message.html' , context)
            
    
    return render(request, template_name='accounts/login.html') 


def uniqueUserName(uname):
    users = User.objects.all()
    usernames = [user.username for user in users]

    if uname in usernames:
        return False
    return True

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                context = { 
                    'title':'Fail!',
                    'm1': 'wrong password or username does not exists',
                    'url':'home',
                }
                return render(request , 'notification/message.html' , context)

        
        return render(request, template_name='accounts/login.html')
    
    

@login_required(login_url='login')
def logOutUser(request):
    auth.logout(request)
    return redirect('/')





@login_required(login_url='login')
def profileUpdate(request):
    formU = UserForm()
    formP = ProfileForm()
    user = User.objects.get(username = request.user.username)
    print(user)

    pro = Profile.objects.get( user = user)
    print(pro)
    formU = UserForm(instance = user)
    formP = ProfileForm(instance = pro)
    if request.method == 'POST':
        formU = UserForm(request.POST, request.FILES, instance=user)
        formP = ProfileForm(request.POST, request.FILES, instance=pro)
        if formP.is_valid():
            formP.save()
        if formU.is_valid():
            formU.save()
        context = { 
            'title':'Successfull',
            'm1': request.user.username,
            'm2':'your profile Update Successfull',
            'url':'userProfile',
            }
        return render(request , 'notification/message.html' , context)

    context = {
        'formP':formP,
        'formU':formU
    }

    return render(request, 'update/profileUpdate.html',context)


# @login_required(login_url='login')
# def changePassword(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # prevent logout
#             context = {
#                 'title': 'Successful',
#                 'm1': 'Password changed successfully',
#                 'url': 'home',
#             }
#             return render(request, 'notification/message.html', context)
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(user=request.user)
    
#     return render(request, 'update/changePassword.html', {'form': form})


@login_required
def settings_view(request):
    if request.method == 'POST':
        formU = UserForm(request.POST, instance=request.user)
        formP = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if formU.is_valid() and formP.is_valid():
            formU.save()
            formP.save()
            messages.success(request, "Your profile has been updated.")
            context = { 
            'title':'Successfull',
            'm1': request.user.username,
            'm2':'your profile Update Successfull',
            'url':'userProfile',
            }
            return render(request , 'notification/message.html' , context)
            
    else:
        formU = UserForm(instance=request.user)
        formP = ProfileForm(instance=request.user.profile)

    password_form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/settings.html', {
        'formU': formU,
        'formP': formP,
        'form': password_form,
    })
    
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            context = {
                'title': 'Successful',
                'm1': 'Your password was successfully updated!',
                'url': '/',
            }
            return render(request, 'notification/message.html', context)
            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/settings.html', {
        'form': form,
    })
    
@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')  

@login_required(login_url='login')
def rateDriver(request,id,scheduleid):
    user = User.objects.get(username = id)
    profile = Profile.objects.get(user = user)
    print(profile)
    schedule = Schedule.objects.get(pk=scheduleid)
    context={
        'id': id,
        'scheduleid':scheduleid,
    }
    if request.method == 'POST':
        rating = request.POST.get('rate') 
        profile.increase_rating(rating)
        profile.increase_service(schedule)
        profile.save()
        
        profile = request.user.profile
        profile.increase_service(schedule)
        profile.save()
        
        schedule.delete()
        
        return render (request, template_name='pages/home.html')
    
    
    else:
    # Optionally return an error or message
        messages.error(request, "Please select a star rating before submitting.")
    
    return render(request, 'pages/rateDriver.html',context)



def ai(request):
     return render (request, template_name='accounts/gemini.html')

