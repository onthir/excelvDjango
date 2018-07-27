from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
import datetime

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'type':'password'}))
    class Meta:
        model = User
        fields =('username', 'email', 'password1', 'password2')
