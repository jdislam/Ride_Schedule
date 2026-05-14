from django import forms
from django.forms import ModelForm
from .models import *


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


        
        
class ProfileForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'country', 'image', 'birthday']

class ChangePassword(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
