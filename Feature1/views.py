from django.shortcuts import redirect, render
from account.models import CASE, Connection, File, Lawyer,User, Client
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .recommend import get_recommendations, preprocess
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

# def log(request):
#     return render(request,"log.html",{'active': 'log'})

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
    sortedlawyers=sorted(approvedLawyer,key=lambda x: x.ratings,reverse=True)
    return render(request,"Lawyer/index-1.html",{"lawyers":sortedlawyers,'a':True})

def lawyer(request,num):
    data=Lawyer.objects.get(user_id=num)
    cases=CASE.objects.filter(lawyer_id=num,case_approval=True,is_running=False)
    woncases=CASE.objects.filter(lawyer_id=num,case_approval=True,is_running=False,case_status="VICTORY")
    try:
        sum=format(woncases.count()*100/cases.count(),".2f")
        percentage=(sum)
    except:
        percentage=0
    runningcases=CASE.objects.filter(lawyer_id=num, case_approval=True,is_running=True)
    pastcases=CASE.objects.filter(lawyer_id=num, case_approval=True,is_running=False)   

    return render(request,"lawyer/Lawyer_profile.html",{"data":data,"runningcases":runningcases,"pastcases":pastcases,'percentage':percentage})

def create_file(request):
    if request.method=='POST':
        filetitle=request.POST.get("file_title")
        filedesc=request.POST.get("file_description")
        filetags=request.POST.get("filetags")

        if filetitle =="" or filedesc=="" or filetags is None:
            messages.error(request,"Unable to create file (Empty information cannot be uploaded)")
            return redirect("/createfile")
        currentuser=request.user
        print(currentuser)
        user=Client.objects.get(user_id=currentuser.id)
        file=File.objects.create(client=user,file_title=filetitle,file_description=filedesc,filetags=filetags)
        file.save()
        
        fileinfo=filetitle+" " +filedesc
        case_dict={}
        cases=CASE.objects.filter(case_approval=True,is_running=False,is_rated=True,case_status="VICTORY")
        for case in cases:
                if case.file.filetags==filetags:
                    case_dict[case.id]=case.case_title+" " +case.file.file_description
        lawyer_ids=[]
        # case_id=[]

        # newfileinfo=preprocess(fileinfo)

        # for search in newfileinfo:
        recommendations=get_recommendations(fileinfo, case_dict)
        lawyer_recommendations = {}
        for file_id, similarity in recommendations:
            print(file_id,similarity)
            if similarity>0.1:
                # case_id.append(doc)
                case = CASE.objects.get(id=file_id)
                related_lawyers = case.lawyer.user_id
                lawyer_ids.append(related_lawyers)       

                if related_lawyers not in lawyer_recommendations:
                    lawyer_recommendations[related_lawyers]=(file_id,similarity)
                else:
                    _, current_similarity = lawyer_recommendations[related_lawyers]
                    if similarity > current_similarity:
                        lawyer_recommendations[related_lawyers,similarity]

        sorted_lawyers = Lawyer.objects.filter(user_id__in=lawyer_ids)
        print(lawyer_recommendations)
        if not sorted_lawyers:
            processed_list = preprocess(filetags)
            lawyer_ids = []
            for tag in processed_list:
                lawyer = Lawyer.objects.filter(specialization_tags__icontains=tag)
                for l in lawyer:
                    lawyer_ids.append(l.user_id)
                
            filtered_lawyers = Lawyer.objects.filter(user_id__in=lawyer_ids)
            sorted_lawyers=filtered_lawyers.order_by("-ratings")
        print(sorted_lawyers)
        return render(request,"client/recommended_lawyers.html",{'lawyers':sorted_lawyers,'lawyer_recommendations':lawyer_recommendations})
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
            if request.method=="POST":
                action=request.POST.get("action")
                act=action.split(" ")
                print(act)
                if act[0]=="Delete":
                    deletethefile=File.objects.filter(file_id=act[1]).first()
                    deletethefile.delete()
                return redirect('/my_profile',{'user':current_user,'files':pastfile,'a':True})
            return render(request,"client/client_profile.html",{'user':current_user,'files':pastfile,'a':True})
        # return render(request,"client/client_profile.html",{'user':current_user})
    
    
    lawyer = Lawyer.objects.filter(user_id=user.id).first()
    if lawyer:
        cases=CASE.objects.filter(lawyer_id=lawyer.user_id,case_approval=True)
        ratedcases=CASE.objects.filter(lawyer_id=lawyer.user_id,case_approval=True,is_running=False,is_rated=True)
        totalcase=(ratedcases.count())
        totalratings=0
        try:
            for i in ratedcases:
                totalratings=totalratings+i.ratings
            rate=format(totalratings/totalcase,".2f")
            lawyer.ratings=rate
            lawyer.save()
        except:
            lawyer.ratings=totalratings
            lawyer.save()            

        pastcases=CASE.objects.filter(lawyer_id=lawyer.user_id, case_approval=True,is_running=False)
                
        try:
            victorycases=CASE.objects.filter(lawyer_id=lawyer.user_id,case_approval=True,is_running=False,case_status="VICTORY")
            noofwins=victorycases.count()
            winpercentage=format((noofwins*100/pastcases.count()),".2f")
        except:
            winpercentage="N/A"
        if(request.method=="POST"):
            result=request.POST.get("result")
            res=result.split(" ")
            file_id=res[1]
            case=CASE.objects.filter(file_id=file_id,case_approval=True).first()
            if(res[0]=="V"):
                case.case_status="VICTORY"
            elif(res[0]=="D"):
                case.case_status="DEFEAT"
            print(case.case_status)
            case.status_saved=True
            case.save()
            return redirect("/my_profile")
        runningcases=CASE.objects.filter(lawyer_id=lawyer.user_id, case_approval=True,is_running=True)
        return render(request,"lawyer/lawyer_myprofile.html",{'user':lawyer,'cases':cases,'a':False,'runningcases':runningcases,'pastcases':pastcases,'winpercentage':winpercentage})
        
    return render(request,"auth/404.html")


def editprofile(request):
    client=request.user
    user=Client.objects.filter(user_id=client.id).first()
    if user:
        if request.method=="POST":
            location=request.POST.get("location")
            phone=request.POST.get("phone")
            if location:
                user.location=location
            if phone:
                user.phone=phone
            user.save()
            return redirect('/my_profile')
        return render(request,"client/edit_profile.html",{'user':user})
    else:
        user=Lawyer.objects.filter(user_id=client.id).first()
        if request.method=="POST":
            location=request.POST.get("location")
            phone=request.POST.get("phone")
            specialization_tags=request.POST.get("specialization_tags")
            profile_description=request.POST.get("profile_description")

            if location:
                user.location=location
            if phone:
                user.phone=phone
            if specialization_tags:
                user.specialization_tags=specialization_tags
            if profile_description:
                user.profile_description=profile_description
            user.save()
            return redirect('/my_profile')
        return render(request,"lawyer/edit_profile.html",{'user':user})

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
        messages.info(request,"Case Request send Successfully")
        return redirect("/my_profile")
    return render(request,"auth/lawyerconnect.html",{'lawyer':lawyer,'files':files})


def connectClient(request):
    # user=request.user
    # if(Client.objects.filter(user_id=user.id)):
    #     a=True
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
            return redirect("/Lawyer/connectClient")
        else:
            messages.error(request,"Case file Discarded !!")
            connect=Connection.objects.filter(case=btnaction[1]).first()
            connect.connect_status=False
            connect.is_removed=True
            connect.save(is_removed=True)
            # connect.delete()
            return redirect("/Lawyer/connectClient")
        
    return render(request,"lawyer/connectClient.html",{'connection':connection})


def PastCases(request):
    currentuser=request.user
    print(currentuser)
    if Lawyer.objects.filter(user_id=currentuser.id):
        cases=CASE.objects.filter(case_approval=True)
        print(cases)
        return render(request,"auth/approved_cases.html",{'cases':cases})

    return render(request,"auth/approved_cases.html")

def acceptedCases(request):

    connections=Connection.objects.filter(client_id=request.user.id,connect_status=True)
    cases=[connection.case for connection in connections]
    flag=False
    if request.method=="POST":
        for case in cases:
            rate=request.POST.get("rating_"+str(case.file_id))
            if rate is not None:
                rating_id=rate.split(" ")
                rating=rating_id[0]
                file_id=rating_id[1]
                case=CASE.objects.filter(file_id=file_id,case_approval=True).first()
                case.ratings=rating
                case.is_rated=True
                case.save()
                print(case)
                lawyer=case.lawyer
                try:
                    allcases=CASE.objects.filter(lawyer_id=lawyer.user_id,case_approval=True,is_rated=True,is_running=False)
                    count=allcases.count()
                    totalrating=0
                    for case in allcases:
                        totalrating=totalrating+case.ratings
                    avgrating=totalrating/count
                    lawyer.ratings=avgrating
                    lawyer.save()
                except:
                    pass
            else:
                pass
        return redirect("/acceptedCases",{'flag':True})
    return render(request, "client/acceptedCases.html",{'cases':cases,'a':True,'flag':flag})

def casestatus(request):

    if request.method=="POST":
        case_status=request.POST.get("case_status")
        running=request.POST.get("is_running")
        fileid=request.POST.get("fileid")
        currentcase=CASE.objects.filter(file_id=fileid).first()
        currentcase.is_running=running        
        if(case_status is None):
            pass
        else:
            currentcase.case_status=case_status
        print(currentcase)
        currentcase.save()
        return redirect('/my_profile')
    cases=CASE.objects.filter(lawyer_id=request.user.id,case_approval=True)
    return render(request,'lawyer/casestatus.html',{'cases':cases})