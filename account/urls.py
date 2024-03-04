from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('register/lawyer/', views.lawyer_registration, name='lawyer_registration'),
    path('register/client/', views.client_registration, name='client_registration'),
]
