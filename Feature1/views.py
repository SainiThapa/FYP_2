from django.shortcuts import redirect, render
from account.models import File, Lawyer,User, Client
from django.contrib.auth.decorators import login_required

# Create your views here.

def handle_404(request, exception):
    return render(request, '404.html', status=404)

def login(request):
    return render(request, 'auth/signin_form.html')

def signup(request):
    return render(request,"signup.html")

def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'lawyer':
            return redirect('/account/register/lawyer')
        elif user_type == 'client':
            return redirect('/account/register/client')
    return render(request, 'choose.html')

def index(request):
    return render(request, "index.html", {'active': 'home'})

def contact(request):
    return render(request, "contact.html", {'active': 'contact'})

def log(request):
    return render(request,"log.html",{'active': 'log'})

def help(request):
    return render(request,"help.html",{'active': 'about'})

def lawyer_list(request):
    lawyers=Lawyer.objects.all()
    approvedLawyer=[]
    for lawyer in lawyers:
        if(lawyer.license_verify_status):
            approvedLawyer.append(lawyer)
    return render(request,"Lawyer/index-1.html",{"lawyers":approvedLawyer})

def lawyer(request,num):
    data=Lawyer.objects.get(user_id=num)
    return render(request,"lawyer/Lawyer_profile.html",{"data":data})

def create_file(request):
    if request.method=='POST':
        filedesc=request.POST.get("file_description")
        currentuser=request.user
        print(currentuser)
        for user in Client.objects.all():
            if currentuser.username ==user.username:
                file=File.objects.create(client=user,file_description=filedesc)
                file.save()
                return redirect('/my_profile')
    return render(request,"client/Create_file.html")


def my_profile(request):

    user=request.user
    Files=File.objects.all()
    pastfile=[]
    for client in Client.objects.all():
        if client.username == user.username:
            current_user=client
            for file in Files:
                if file.client.username==user.username:
                    print(file)
                    pastfile.append(file)
            return render(request,"client/client_profile.html",{'user':current_user,'files':pastfile})
        # return render(request,"client/client_profile.html",{'user':current_user})
    
    for lawyer in Lawyer.objects.all():
        if lawyer.username == user.username:
            current_lawyer=lawyer
            return render(request,"lawyer/lawyer_myprofile.html",{'user':current_lawyer})
        
    return render(request,"auth/404.html")
