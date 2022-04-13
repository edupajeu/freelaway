from django.urls import path
from . import views  # THE DOT MEANS THE SAME FOLDER TO IMPORT

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
