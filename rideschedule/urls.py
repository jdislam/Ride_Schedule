"""
URL configuration for rideschedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views as b_view
from accounts import views as a_view
from schedules import views as s_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',b_view.home,name='home'),
    path('home',b_view.home,name='home'),
    
    path('loginUser',a_view.loginUser,name='loginUser'),
    path('logOutUser', a_view.logOutUser, name='logOutUser'),
    path('createRider', a_view.createRider , name = 'createRider'),
    path('profileUpdate', a_view.profileUpdate, name='profileUpdate'),
    path('settings', a_view.settings_view, name='settings'),
    path('settings/change-password/', a_view.change_password_view, name='changePassword'),
    path('settings/delete/', a_view.delete_account_view, name='deleteAccount'),
    
    
    
    path('weeklySchedule',s_view.weeklySchedule,name='weeklySchedule'),
    path('dailySchedule',s_view.dailySchedule, name='dailySchedule'),
    path('monthlySchedule',s_view.monthlySchedule, name='monthlySchedule'),
    path('parcelDelivery',s_view.parcelDelivery,name='parcelDelivery'),
    path('courier',s_view.courier,name='courier'),
    path('pharmacy',s_view.pharmacy,name='pharmacy'),
    path('allService',s_view.allService, name='allService'),
    
    path('userProfile',a_view.userProfile,name='userProfile'),
    
    path('schedulePost',s_view.schedulePost,name = 'schedulePost'),
    path('userPost',s_view.userPost,name = 'userPost'),
    path('takeSchedule <str:id>',s_view.takeSchedule,name='takeSchedule'),
    path('deleteSchedule <str:id>',s_view.deleteSchedule,name='deleteSchedule'),
    path('completeSchedule <str:id>',s_view.completeSchedule,name='completeSchedule'),
    path('updateSchedule <str:id>',s_view.updateSchedule,name='updateSchedule'),
    
    path('policy', b_view.policy, name = 'policy'),
    path('rateUs', b_view.rateUs, name = 'rateUs'),
    path('rateDriver <str:id> <str:scheduleid>', a_view.rateDriver, name = 'rateDriver'),
    path('help', b_view.help , name = 'help'),
    path('contact', b_view.contact , name = 'contact'),
    path('joinHelp', b_view.helpToJoin, name='joinHelp'),
    
    path('readHistory',s_view.readHistory,name = 'readHistory'),
    path('deleteHistory <str:id>', s_view.deleteHistory, name='deleteHistory'),
    path('deleteAllHistory',s_view.deleteAllHistory,name = 'deleteAllHistory'),
    path('deleteAllNotification',s_view.deleteAllNotification,name = 'deleteAllNotification'),
   
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)