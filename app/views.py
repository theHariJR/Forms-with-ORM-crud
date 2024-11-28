from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration(request):
    if request.method=='POST' and request.FILES:

        NMUFDO=UserForm(request.POST)                           #NON MODIFY-ABLE USER FORM DATA OBJECT
        NMPFDO=ProfileForm(request.POST, request.FILES)         #NON MODIFY-ABLE PROFILE FORM DATA OBJECT
        if NMUFDO.is_valid() and NMPFDO.is_valid():

            # USER FORM
            MUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            # PROFILE FORM
            MPFDO=NMPFDO.save(commit=False)
            MPFDO.user_name=MUFDO
            MPFDO.save()

            send_mail(
                'Interview Results',
                'Dear Sandeep Samal, we are delighted to announce that you have be selected for the role of ASSOCIATE SOFTWARE ENGINEER. Further details regarding Date of onboarding and Salary structure will be communicated in short time. We request you to frequently check your mailbox within next few days. Excited to see you in-office!',
                'iamsrihari10@gmail.com',
                [MUFDO.email],
                fail_silently=False)

            return HttpResponse('Registration Done Successfully!')
        else:
            return HttpResponse('Registration Not Done. Error!')
        
    d={'UF': UserForm(), 'PF': ProfileForm()}
    return render(request, 'registration.html', d)


# HOME PAGE
def home(request):
    d={}
    if request.session.get('username'):
        username=request.session.get('username')
        
        d={'username': username}
    return render(request, 'home.html', d)
    # return render(request, 'home.html')

# LOGIN PAGE
def user_login(request):
    if request.method=='post':
        name=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=name, password=password)
        if AUO:
            if AUO.is_active:
                login(request, AUO)
                request.session['username']=name
                return HttpResponseRedirect(reverse('home'))
            else:
                HttpResponse('Not an active User. Check your credentials again')
        else:
            HttpResponse('Invalid Data!')

    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
