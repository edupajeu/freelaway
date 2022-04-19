from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from jobs.models import Jobs
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login')
def find_jobs(request):
    if request.method == "GET":
        # RANGE OF PRICES
        min_price = request.GET.get('minimum_price')
        max_price = request.GET.get('maximum_price')
        # RANGE OF TIME
        min_time = request.GET.get('minimum_time')
        max_time = request.GET.get('maximum_time')
        # LIST OF CATEGORIES
        cat = request.GET.get('category')

        if min_price or max_price or min_time or max_time or cat:
            if not min_price:
                min_price = 0

            if not max_price:
                max_price = 99999

            if not min_time:
                min_time = datetime(year=1900, month=1, day=1)  # DATETIME DEALING WITH DATE AND TIME

            if not max_time:
                max_time = datetime(year=3000, month=1, day=1)

            # DEALING WITH CATEGORY FIELD AND PUT INTO A LIST
            if cat == 'D':
                cat = ['D', ]
            elif cat == 'VE':
                cat = ['VE']

            # __gte IT MEANS GREATER THAN AND __lte IT MEANS GREATER THAN
            jobs = Jobs.objects \
                .filter(price__gte=min_price) \
                .filter(price__lte=max_price) \
                .filter(delivery_time__gte=min_time) \
                .filter(delivery_time__lte=max_time) \
                .filter(category__in=cat) \
                .filter(private=False)

        else:
            jobs = Jobs.objects.filter(private=False)
        return render(request, 'find_jobs.html', {'jobs': jobs})  # JOBS IS REFERRED TO FIND_JOBS.HTML


@login_required(login_url='/auth/login')
def accept_job(request, id):
    job = Jobs.objects.get(id=id)
    job.professional = request.user  # UPDATE DATABASE JOBS
    job.private = True
    job.save()
    return redirect('/jobs/find_jobs')


@login_required(login_url='/auth/login')
def profile(request):
    if request.method == "GET":
        jobs = Jobs.objects.filter(professional=request.user)  # FILTERING BY PROFESSIONAL
        return render(request, 'profile.html', {'jobs': jobs})
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username=username).exclude(
            id=request.user.id)  # EXCLUDE ALLOW US REUSE THE SAME USER

        if user.exists():
            messages.add_message(request, constants.ERROR, 'It already exists a user with this Username')
            return redirect('/jobs/profile')

        user = User.objects.filter(email=email).exclude(id=request.user.id)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'It already exists a user with this E-mail')
            return redirect('/jobs/profile')

        request.user.username = username
        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        messages.add_message(request, constants.SUCCESS, 'Update successfully done!')
        return redirect('/jobs/profile')


@login_required(login_url='/auth/login')
def send_project(request):
    file = request.FILES.get('file')
    id_job = request.POST.get('id')

    job = Jobs.objects.get(id=id_job)

    job.final_file = file
    job.status = 'WA'
    job.save()
    return redirect('/jobs/profile')
