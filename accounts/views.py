from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib import auth
from .models import user_profile


# Create your views here.
def signup(request):
    if request.method == 'POST':
        # user has info and wants an account now else
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username']) # checking to see if username is taken or not
                return render(request,'accounts/signup.html',{'error':'Username has aldready been taken'})
            except User.DoesNotExist:
                #making 2 instances in total
                if '@jpischool' in request.POST['email']:
                    if (int(request.POST['grade']) > 0) and (int(request.POST['grade']) < 13):
                        if ('test1' in request.POST['username']):
                            user = User.objects.create_user(username = request.POST['username'],password = request.POST['password1'],email = request.POST['email'])
                            user_info = user_profile()
                            user_info.grade = request.POST['grade']
                            user_info.is_student = True
                            user_info.hunter = user
                            user_info.save()
                            subject = 'Welcome to JPIS Complaint Manager{}'.format( request.POST['username'])
                            message = 'Thank you for logging in. You can now use this website'
                            from_email = settings.EMAIL_HOST_USER
                            to_list = [user.email, settings.EMAIL_HOST_USER]
                            send_mail(subject,message,from_email, to_list, fail_silently = False)
                            auth.login(request,user)
                            return redirect('home')
                        else:
                            return render(request,'accounts/signup.html',{'error':"User does not exist in hostel database"})
                    else:
                        return render(request,'accounts/signup.html',{'error':"invalid grade"})
                else:
                    return render(request,'accounts/signup.html',{'error':"username must be @jpischool.com"})
        else:
            return render(request,'accounts/signup.html',{'error':"Passwords don't match "})
    else:
        return render(request,'accounts/signup.html')

def signup_admin(request):
    if request.method == 'POST':
        # user has info and wants an account now else
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username']) # checking to see if username is taken or not
                return render(request,'accounts/signup.html',{'error':'Username has aldready been taken'})
            except User.DoesNotExist:
                #making 2 instances in total
                user = User.objects.create_user(username = request.POST['username'],password = request.POST['password1'],email = request.POST['email'])
                user_info = user_profile()
                user_info.grade = request.POST['grade']
                user_info.is_admin = True
                user_info.hunter = user
                user_info.save()
                auth.login(request,user)

                return redirect('home')
        else:
            return render(request,'accounts/signup_admin.html',{'error':"Passwords don't match "})
    else:
        return render(request,'accounts/signup_admin.html')



def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username = request.POST['username'] ,password = request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
            #check whether a user is registered
        else:
            return render(request,'accounts/login.html',{'error':'username or password is incorrect'})
    else:
        # In case the user doesn't want to post a specific request
        return render(request,'accounts/login.html' )

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

# Create your views here.
