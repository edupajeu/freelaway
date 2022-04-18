from datetime import datetime
from django.shortcuts import render
from jobs.models import Jobs


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
            jobs = Jobs.objects\
                .filter(price__gte=min_price) \
                .filter(price__lte=max_price) \
                .filter(delivery_time__gte=min_time) \
                .filter(delivery_time__lte=max_time) \
                .filter(category__in=cat) \
                .filter(private=False)

        else:
            jobs = Jobs.objects.filter(private=False)
        return render(request, 'find_jobs.html', {'jobs': jobs})  # JOBS IS REFERRED TO FIND_JOBS.HTML
