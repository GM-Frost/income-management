from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain [A-z] or [0-9] Characters'},status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry! Username is already in use, choose another one'},status=409)

        return JsonResponse({'username_valid':True})
    
class EmailValidationView(View):

    def post(self,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry! This Email Already Exists'},status=409)
        
        return JsonResponse({'email_valid':True})
    
class RegistrationView(View):

    def get(self,request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #GET USER DATA
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }
            
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password too Short. Please try again')
                    return render(request, 'authentication/register.html',context)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                messages.success(request,'Accout Registered Successfully')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome, "+user.username+" you are now logged in")
                    return redirect('expenses')
                else:
                    messages.error(request,"Account is not active, please ask the admin")
                    return render(request, 'authentication/login.html')

            messages.error(request,"Invalid Credentials, try again")
            return render(request, 'authentication/login.html')
        
        messages.error(request,"Please Fill All the fields")
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request,'You have been logged out')
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request,'authentication/reset-password.html')
    
    def post(self,request):
        email = request.POST['email']

        if not email:
            messages.error(request,'Please Enter valid Email Address')
            return render(request,'authentication/reset-password.html')

        else:
            user =  User.objects.filter(email=email)

            if user.exists():
                messages.info(request,'Please Check your Email for Futher Process')
                return render(request,'authentication/reset-password.html')
            else:
                messages.error(request,'Email Address not found')
                return render(request,'authentication/reset-password.html')



            
            
            

