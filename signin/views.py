from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password

from signin2.settings import EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER='djangoprojects7@gmail.com'

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=="POST":
        firstName=request.POST.get("fname")
        lastName=request.POST.get("lname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        password2=request.POST.get("password2")


        if not firstName.isalpha() and  not lastName.isalpha():
            messages.warning(request, "name must contain letters only")
            return render(request, 'register.html')


        if len(password)<8 and len(password2)<8:
            messages.warning(request, "password must be atleast 8 characters")
            return render(request, 'register.html')


        if password!=password2:
            messages.warning(request,"both passwords are not mathching")
            return render(request, 'register.html')

        if User.objects.filter(email=email):
            messages.warning(request, "email already registered! please signin")
            return render(request,'register.html')

        username=firstName+" "+lastName
        newuser=User.objects.create_user(username=username,first_name=firstName,last_name=lastName,email=email,password=password,is_staff=True)
        newuser.first_name=firstName
        newuser.last_name=lastName
        newuser.email=email
        newuser.password=password
        newuser.username=username
        newuser.is_active=True
        #newuser.set_password(password)
        newuser.save()
        return render(request,'signin.html')

    return render(request,'register.html')

def signin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        #messages.success(request,make_password(password))
        username=request.POST.get("username")
        usertype=request.POST.get("admin")
        '''if len(password)<=7:
            messages.warning(request,"password must be atleast 8 characters")
            return render(request,'signin.html')'''


        if email is None:
            messages.success(request,"Logged out")
            return render(request, 'signin.html')


        user=User.objects.filter(username=username)
        '''if user is not None:
            messages.success(request,"hiiiii"+username)'''
        if usertype!="admin":
            existedUser = User.objects.filter(username=username, email=email,password=password).first()
        else:
            existedUser = authenticate(username=username, email=email, password=password)
            login(request, existedUser)


        if  existedUser:
                login(request,existedUser)
                messages.success(request,"logged in.")
                return render(request,'dashboard.html',{'user':existedUser,'email':email})


        if existedUser is None:
            messages.warning(request,"Please enter email and password correctly!")
            #return render(request,'signin.html')

    return render(request,'signin.html')

def show(request):
    users=get_user_model().objects.all()
    return render(request,'show.html',{'users':users})

def signout(request):

    logout(request)
    messages.success(request,"Logged out.")
    return render(request,'index.html')


def changepassword(request,email):
    if request.method=="POST":
        newpassword=request.POST.get("newpassword")
        newpassword2= request.POST.get("newpassword2")

        if newpassword!=newpassword2:
            messages.warning(request,"both passwords did not match ")
            return render(request,'changepassword.html')

        elif newpassword2==newpassword:
            user=User.objects.get(email=email)
            user.password=newpassword;
            user.save()
            messages.success(request,"password is sucessfully updated!")
            return render(request,'signin.html')

    return render(request,'changepassword.html',{'email':email})



def otp(request):

    return HttpResponse("hiiiii")
