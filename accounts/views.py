from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . forms import *
from analyze.models import *

# Create your views here.
def home(request):
    return render(request, 'accounts/homepage.html')


'''
REGISTER NEW USER
#REGISTER ACCOUNT USING USER CREATION FORM WITH DEFAULT USER MODEL
'''

def register_account(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == 'POST':
            form  = UserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                credentials = form.save()

                # get username and password to login the user
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                return redirect("accounts:home")
        else:
            form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_user(request):

    if request.user.is_authenticated:
        return redirect("accounts:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('analyze:home')
                else:
                    return render(request, 'accounts/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'accounts/login.html', {'error_message': 'Invalid username or password'})
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect("accounts:login")


def profile(request, user):
    if request.user.is_authenticated:
        userObj = User.objects.get(username=user)
        files = File.objects.filter(user=userObj)

        context = {
            'files': files,
            'user': user,
        }
        return render(request, 'accounts/userprofile.html', context)
    else:
        return rendirect("accounts:login")


"""
DELETE USER
CLEANER VIEW EXCEL
CSV COMPARISION

"""