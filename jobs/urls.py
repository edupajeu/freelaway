from django.urls import path
from . import views  # THE DOT MEANS THE SAME FOLDER TO IMPORT
from django.contrib.auth import views as auth_views  # VIEWS THAT COME FROM CONTRIB.AUTH AND ALIENED AS AUTH_VIEWS


urlpatterns = [
    path('find_jobs/', views.find_jobs, name='find_jobs'),
    ]
