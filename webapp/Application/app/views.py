"""
Definition of views.
"""
from django.contrib.auth.models import User,auth
from django.shortcuts import render ,redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import User_profile
from django.contrib import messages

# def home(request):
#     """Renders the home page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/userHome.html',
#         {
#             'title':'Home Page',
#             'year':datetime.now().year,
#         }
#     )

# def contact(request):
#     """Renders the contact page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         }
#     )

# def about(request):
#     """Renders the about page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/about.html',
#         {
#             'title':'About',
#             'message':'Your application description page.',
#             'year':datetime.now().year,
#         }
#     )

def home(request):
    #return HttpResponse("Hello. This is the page in app")
    return render(request,'app/userHome.html')


def login(request):
    if request.method == 'POST':
       username=request.POST['username']
       pwd =request.POST['password']
        
       #user = auth.authenticate(username=username,password=password)
    #user = User_profile.objects.filter(email=username,password=pwd).exists()
       user = User_profile.objects.filter(email=username,password=pwd)
       if user is not None:
          return render(request,'app/userhomepage.html',{'Uname':user.get().first_name})
       else:
            messages.info(request,'invalid credentials ')
            return render(request,'app/login1.html')
    else:
         return render(request,'app/login1.html')

def logout(request):
    return render(request,'app/login1.html')

def register(request):
    if  request.method == 'POST':
          fName =request.POST['first_name']
          lName =request.POST['last_name']
          emailId =request.POST['email']
          pwd =request.POST['password']
          confirmPassword =request.POST['confirmPassword']
       
          if pwd==confirmPassword:
             if User.objects.filter(email=emailId).exists():
                  messages.info(request ,'Email Taken')
                  return redirect( 'register')
             else:
                  user = User_profile.objects.create(first_name=fName,last_name=lName,email=emailId,password=pwd,confirm_password=confirmPassword)
                  user.save()
                  print ('user created')
                  return render(request,'app/login1.html')
          else:
                messages.info(request,'password not matching...' )
                return redirect( 'register')
          return redirect( 'register')

    else:
       return render(request , 'app/register.html')    