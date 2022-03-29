from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import DentistProfile
from django import forms
from account.models import Account
#Create forms here

class CreateUserForm(UserCreationForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','username','email','password1','password2']

class DentistProfileForm(forms.ModelForm):
    class Meta:
        model = DentistProfile
        fields=("Clinic","Address1","Address2","City","Postcode","Country")