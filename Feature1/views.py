from django.shortcuts import redirect, render

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
    return render(request,"index.html",{'active': 'home'})

def contact(request):
    return render(request,"contact.html",{'active': 'contact'})

def log(request):
    return render(request,"log.html",{'active': 'log'})

def help(request):
    return render(request,"help.html",{'active': 'about'})
