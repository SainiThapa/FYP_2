from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Lawyer import settings
from account.models import Client
from .forms import ClientSignupForm, LawyerSignupForm
# import bcrypt

def signup(request):
     return render(request,"signup.html")

def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'lawyer':
            return redirect('lawyer_registration')
        elif user_type == 'client':
            return redirect('client_register')
    return render(request, 'login.html')


def client_registration(request):
    if request.method == 'POST':
        user_form = ClientSignupForm(request.POST)
        profile_form = ClientSignupForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
            # username=request.POST.get("name")
            # password=request.POST.get("password")
            # email=request.POST.get("email")
            # location=request.POST.get("location")
            # profile_pic=request.POST.get("profile_picture")
            # phone=request.POST.get("phone")

            # client = User.objects.create_user(username,bcrypt.hashpw(password),email,location,profile_pic,phone)
            # client.save()
            # return redirect('login')
        # else:
        #     messages.info("Error creating the user")
        #     # return False
    else:
        form = ClientSignupForm()
    return render(request, 'client_registration.html', {'form': form})

# def client_register(request):

    if request.method=='POST':
        Clientname=request.POST.get('name')
        profile_picture=request.POST.get('profile_picture')
        location=request.POST.get('location')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password1=request.POST.get('password')
        password2=request.POST.get('confirm_password')
        
        if profile_picture:
             pass
        else:
             profile_picture=settings.STATIC_URL+"img/blank.webp"

        if Clientname=='' or phone=='' or email=='' or location=='' or password1=='' or password2=='':
            messages.info(request,"Make sure to fill all the boxes !!")
            return redirect('client_register')
        else:
            if (password1==password2):
                if Client.objects.filter(name=Clientname).exists():
                    messages.info(request,"Username already taken !!")
                    return redirect('/account/register/client')
                elif Client.objects.filter(email=email).exists():
                    messages.info(request,'Email already in use !!')
                    return redirect('client_register')
                else:
                                client=Client.objects.create(name=Clientname, profile_picture=profile_picture,location=location,phone=phone,password=password1, email=email)
                                client.save()
                                print('USER CREATED !')
                                return redirect('login')
            else:
                messages.info(request,"Password doesnot match !!")
                return redirect('client_register')
    else:
        return render(request,"client_registration.html")
    
def lawyer_registration(request):
    if request.method == 'POST':
        LawyerName=request.POST.get('name')
        profile_picture=request.POST.get('profile_picture')
        location=request.POST.get('location')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password1=request.POST.get('password')
        password2=request.POST.get('confirm_password')


