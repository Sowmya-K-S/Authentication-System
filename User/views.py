# import section
from django.shortcuts import render,redirect

# importing random function
from random import randint

# importing settings.py
from django.conf import settings

# for email utility
from django.core.mail import send_mail

#importing DB tables from models.py
from User.models import Users


# Create your views here.

from django.utils import timezone 
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'login.html')
    
def register(request):
    global c_otp
    # when we click on register option
    if request.method == 'GET':
        return render(request, 'register.html')
    
    # when we click on register button
    else:
       
        # checking whether the entered email is already used for registration
        try:
            # error occurs when there is no email match
            # then control goes to except block

            Users.objects.get(email = request.POST['email'])
            return render(request,'register.html',{'msg':"Email already registered, try using other Email"})
        
        except:
            # validating password and confirm password
            if request.POST['password'] == request.POST['cpassword']:
                #  generating otp
                global c_otp
                c_otp = randint(100_000,999_999)

                #extracting data from registration form
                global reg_form_data 

                reg_form_data = {
                    "full_name" : request.POST['full_name'],
                    "gender" : request.POST['gender'],
                    "age" : request.POST['age'],
                    "email" : request.POST['email'],
                    "phoneno" : request.POST['phoneno'],
                    "password" : request.POST['password'],
                }

                # sending the generated OTP via mail
                subject = "Registration"
                message = f'Hello{reg_form_data["full_name"]}, Welcome. Your OTP is {c_otp}'
                sender = settings.EMAIL_HOST_USER
                receiver = [reg_form_data['email']]
                send_mail(subject, message, sender, receiver)

                #after sending OTP render the page to enter OTP
                return render(request,'otp.html')

            else:
                return render(request, 'register.html',{'msg':"Both Passwords didn't match"})
            
def otp(request):
    if str(c_otp) == request.POST['u_otp']:
        Users.objects.create(full_name=reg_form_data['full_name'], gender = reg_form_data['gender'], age = reg_form_data['age'], email = reg_form_data['email'], phoneno = reg_form_data['phoneno'],password = reg_form_data['password'])
        return render(request,'register.html', {'msg': "Registration Successfull !! Account created"})
    else:
        return render(request, 'otp.html',{'msg':"Invalid OTP"})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            # finding the record of person trying to login in database
            session_User = Users.objects.get(email = request.POST['email'])
            print(session_User)
            if request.POST['password'] == session_User.password:
                request.session['email'] = session_User.email
                return render(request,'index.html')
            else:
                return render(request, 'login.html', {'msg':'invalid password'})
        except:
            return render(request, 'login.html',{'msg': 'This email is not Registered !!'})
    
def logout(request):
    del request.session['email']
    return redirect('login')
