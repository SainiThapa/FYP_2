from django.shortcuts import redirect, render
from account.models import CASE, Connection, File, Lawyer,User, Client
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    currentuser=request.user
    if currentuser:
        if Client.objects.filter(user_id=currentuser.id).first():
            return render(request,"index.html",{'a':True,'b':False})
        if Lawyer.objects.filter(user_id=currentuser.id).first():
            return render(request,"index.html",{'a':False,'b':True})
    return render(request, "index.html")

def contact(request):
    user=request.user
    a=False
    if(Client.objects.filter(user_id=user.id)):
        a=True
    return render(request, "contact.html", {'active': 'contact','a':a})

def log(request):
    return render(request,"log.html",{'active': 'log'})

def help(request):
    user=request.user
    a=False
    if(Client.objects.filter(user_id=user.id)):
        a=True
    return render(request,"help.html",{'active': 'about','a':a})

def lawyer_list(request):
    currentuser=request.user
    if Lawyer.objects.filter(user_id=currentuser.id).first():
        return render(request,"auth/404.html")
    lawyers=Lawyer.objects.all()
    approvedLawyer=[]
    for lawyer in lawyers:
        if(lawyer.license_verify_status):
            approvedLawyer.append(lawyer)
    return render(request,"Lawyer/index-1.html",{"lawyers":approvedLawyer,'a':True})

def lawyer(request,num):
    data=Lawyer.objects.get(user_id=num)
    return render(request,"lawyer/Lawyer_profile.html",{"data":data})

def create_file(request):
    if request.method=='POST':
        filetitle=request.POST.get("file_title")
        filedesc=request.POST.get("file_description")
        filetags=request.POST.get("filetags")

        currentuser=request.user
        print(currentuser)
        user=Client.objects.get(user_id=currentuser.id)
        file=File.objects.create(client=user,file_title=filetitle,file_description=filedesc,filetags=filetags)
        file.save()
        # for user in Client.objects.all():
        #     if currentuser.username ==user.username:
        return redirect('/lawyer_list')
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
            return render(request,"client/client_profile.html",{'user':current_user,'files':pastfile,'a':True})
        # return render(request,"client/client_profile.html",{'user':current_user})
    
    for lawyer in Lawyer.objects.all():
        if lawyer.username == user.username:
            current_lawyer=lawyer
            return render(request,"lawyer/lawyer_myprofile.html",{'user':current_lawyer})
    return render(request,"auth/404.html")

def lawyerconnect(request,num=None):
    currentuser=request.user
    lawyer=Lawyer.objects.filter(user_id=num).first()
    client=Client.objects.filter(user_id=currentuser.id).first()
    files=File.objects.filter(client=currentuser.id)
    if request.method=="POST":
        file_id=request.POST.get("file_id")
        newfile=File.objects.filter(file_id=file_id).first()
        print(newfile.file_title)
        case=CASE.objects.create(file=newfile,lawyer=lawyer,case_title=newfile.file_title)
        case.save()
        print(CASE.objects.all())
        connection=Connection.objects.create(lawyer=lawyer,client=client,case=case)
        connection.save()
        return render(request,"auth/404.html")
    return render(request,"auth/lawyerconnect.html",{'lawyer':lawyer,'files':files})


def connectClient(request):
    user=request.user
    if(Client.objects.filter(user_id=user.id)):
        a=True
    currentuser=request.user
    # connections=Connection.objects.all()
    connection=Connection.objects.filter(lawyer=currentuser.id,is_removed=False)

    if request.method=="POST":
        action=request.POST.get("action")

        btnaction=action.split(" ")
        print(btnaction)
        if(btnaction[0]=="accept"):
            messages.info(request,"Case file Accepted !!")
            connect=Connection.objects.filter(case_id=btnaction[1]).first()
            print(connect)
            connect.connect_status=True
            connect.is_removed=True
            connect.save()
            # connect.delete()
            return redirect("/Lawyer/connectClient",{'a':a})
        else:
            messages.error(request,"Case file Discarded !!")
            connect=Connection.objects.filter(case=btnaction[1]).first()
            connect.connect_status=False
            connect.is_removed=True
            connect.save(is_removed=True)
            # connect.delete()
            return redirect("/Lawyer/connectClient",{'a':a})
        
    return render(request,"lawyer/connectClient.html",{'connection':connection,'a':True})


def PastCases(request):
    currentuser=request.user
    print(currentuser)
    if Lawyer.objects.filter(user_id=currentuser.id):
        cases=CASE.objects.filter(case_approval=True)
        print(cases)
        return render(request,"auth/approved_cases.html",{'cases':cases})

    return render(request,"auth/approved_cases.html")

def acceptedCases(request):

    connections=Connection.objects.filter(client_id=request.user.id)
    cases=[connection.case for connection in connections]

    user=request.user
    a=False
    if(Client.objects.filter(user_id=user.id)):
        a=True
    return render(request, "client/acceptedCases.html",{'cases':cases,'a':True})