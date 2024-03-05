from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from Lawyer import settings
from account.models import Client, Lawyer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


# from .forms import ClientSignupForm, LawyerSignupForm
# import bcrypt

def signup(request):
     return render(request,"signup.html")

def log_in(request):
    if request.method=='POST':
        username=request.POST.get('name','default value')
        password=request.POST.get('password','default value')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            # User found and password matches, log in the user
            auth.login(request, user)
            print("Login successful")
            return redirect('/')
        # print(User.objects.all())
        else:
            messages.error(request,'Invalid Credentials !!')
            print('Try again')
            return redirect('login')
    else:
        return render(request, 'client/loginclient.html')
    
    # return render(request,'client/loginclient.html')

def logout(request):
     auth.logout(request)
     return redirect('/')

def loginlawyer(request):
    return render(request, 'client/loginclient.html')

def client_registration(request):
    if request.method=='POST':
        Clientname=request.POST.get('name')
        profile_picture=request.POST.get('profile_picture')
        location=request.POST.get('location')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if profile_picture:
             pass
        else:
             profile_picture=settings.STATIC_URL+"img/blank.webp"

        if Clientname=='' or phone=='' or email=='' or location=='' or password1=='' or password2=='':
            messages.info(request,"Make sure to fill all the boxes !!")
            return redirect('client_registration')
        else:
            if (password1==password2):
                if User.objects.filter(username=Clientname).exists():
                    messages.info(request,"Username already taken !!")
                    return redirect('/account/register/client')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email already in use !!')
                    return redirect('/account/register/client')
                else:
                                # password=make_password('password1')
                                user=User.objects.create_user(username=Clientname,email=email,password=password1)
                                user.save()
                                client=Client.objects.create(
                                     user=user, username=Clientname, email=email,password=password1,
                                      profile_picture=profile_picture,location=location,phone=phone)
                                client.save()
                                print('USER CREATED !')
                                return redirect('/login')
            else:
                messages.info(request,"Password doesnot match !!")
                return redirect('client_registration')
    return render(request,"client_registration.html")
    
def lawyer_registration(request):
    
    return render(request,"lawyer/Signup.html")



