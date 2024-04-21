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
    auth.logout(request)
    if request.method=='POST':
        name=request.POST.get('name','default value')
        password=request.POST.get('password','default value')
        user=auth.authenticate(username=name,password=password)
        if user is not None:
            # User found and password matches, log in the user
            for object in Client.objects.all():
                if name==object.username:
                    a=True
                    auth.login(request, user)
                    print("Client Login successful")
                    return redirect('/',{'user':user,'a':a})
            for lawyer in Lawyer.objects.all():
                if lawyer.username==name:
                    if lawyer.license_verify_status:
                        a=False
                        auth.login(request,user)
                        print("Lawyer Login Successful")
                        return redirect('/',{'user':lawyer,'a':a})
                    else:
                        return render(request,"lawyer/login.html")
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
        profile_picture=request.FILES.get('profile_picture')
        location=request.POST.get('location')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        

        if Clientname=='' or phone=='' or email=='' or location=='' or password1=='' or password2=='' or profile_picture=="":
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
                                return redirect('/account/login')
            else:
                messages.info(request,"Password doesnot match !!")
                return redirect('account/register/client')
    return render(request,"client/client_registration.html")
    
def lawyer_registration(request):
    if request.method=="POST":
        Lawyername=request.POST.get("name")
        location=request.POST.get('location')
        email=request.POST.get('email')
        profile_picture=request.FILES.get('profile_picture')
        phone=request.POST.get('phone')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        specialization_tags=request.POST.get('specialization_tags')
        profile_description=request.POST.get('profile_description')

        # License
        license_no=request.POST.get('license_no')
        license_img=request.FILES.get('license_img')
        license_verify_status=False
        license_location=request.POST.get('license_location')

        # Academic
        academic_degree=request.FILES.get('academic_degree')
        completion_year=request.POST.get('completion_year')
        major_subject=request.POST.get('major_subject')

        if Lawyername=='' or phone=='' or email=='' or location=='' or password1=='' or password2=='' or profile_picture is None or profile_description=="" or specialization_tags=="" or license_img is None or license_no=="" or license_location=="" or academic_degree is None or completion_year=="" or major_subject=="":
            messages.error(request,"Make sure to fill all the boxes !!")
            # return redirect('/account/register/lawyer')
        else:
             if password1==password2:
                  if User.objects.filter(email=email).exists():
                       messages.error(request,"Email already in use !!")
                       return redirect("/account/register/lawyer")
                  else:
                    user=User.objects.create_user(username=Lawyername,email=email,password=password1)
                    user.is_active = False
                    user.save()
                    lawyer=Lawyer.objects.create(user=user,username=Lawyername,email=email,password=password1,
                    profile_picture=profile_picture,location=location,phone=phone, specialization_tags= specialization_tags,profile_description=profile_description,license_no=license_no,license_img=license_img,license_verify_status=license_verify_status,license_location=license_location,academic_degree=academic_degree,completion_year=completion_year,major_subject=major_subject)
                    lawyer.save()
                    print('LAWYER CREATED !')
                    return redirect('/account/login',{'text':'Waiting for the admin to verify your informations'})
             else:
                  messages.error(request,"Password donot match, Try Again !")
                  return redirect('/account/register/lawyer')                                                                  
    return render(request,"lawyer/Signup.html")



