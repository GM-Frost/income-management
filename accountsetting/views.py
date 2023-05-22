from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def index(request):
    return render(request, 'accountsetting/index.html')
   
class CompletePasswordReset(View):
    def get(self,request):
        messages.success(request,'Password Reset Successful')
        return render(request,'accountsetting/index.html')
    
    def post(self,request):
        
        password = request.POST['password']
        password2 = request.POST['password2']

        if password!=password2:
            messages.error(request,'Password dont Match')
            return render(request,'accountsetting/index.html')

        if len(password)<6:
            messages.error(request,'Password too short')
            return render(request,'accountsetting/index.html')

        messages.success(request,'Password Reset Successful')
        return render(request,'accountsetting/index.html')
