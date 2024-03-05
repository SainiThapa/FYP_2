from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout,name="logout"),
    path('login/', views.log_in, name='login'),
    path('login/lawyer/', views.loginlawyer, name='loginlawyer'),
    path('register/lawyer/', views.lawyer_registration, name='lawyer_registration'),
    path('register/client/', views.client_registration, name='client_registration'),
]
