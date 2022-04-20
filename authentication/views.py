from django.shortcuts import render, redirect
from django.http import HttpResponse  # WE USE TO HAVE THE FUNCTION HTTPRESPONSE IN TESTS
from django.contrib.auth.models import User  # CONTRIB TO USER CONFIRMATION
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def signup(request):
    if request.method == "GET":
        if request.user.is_authenticated:  # VERIFY IF THE USER IS ALREADY AUTHENTICATED
            return redirect('/jobs/find_jobs')
        return render(request, 'signup.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm-password')

        if not password == confirm_pass:
            messages.add_message(request, constants.ERROR, 'The passwords don’t match!')
            return redirect('/auth/signup')

        if len(username.strip()) == 0 or len(password.strip()) == 0:  # USERNAME OR PASSWORD EQUAL ZERO
            messages.add_message(request, constants.ERROR, 'Fill up all the fields!')
            return redirect('/auth/signup')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'This user already exists!')
            return redirect('/auth/signup')

        try:
            user = User.objects.create_user(username=username, password=password)

            user.save()
            messages.add_message(request, constants.SUCCESS, 'User registered')
            return redirect('/auth/login')

        except:
            messages.add_message(request, constants.ERROR, 'Internal system error!')
            return redirect('/auth/signup')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:  # VERIFY IS THE USER IS ALREADY AUTHENTICATED
            return redirect('/jobs/find_jobs')
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username or password invalid')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/jobs/find_jobs')


def logout(request):
    auth.logout(request)
    return redirect('/auth/login')
