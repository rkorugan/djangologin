from django.shortcuts import render
from loginapp.forms import UserForm,UserProfileInfoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import  login,logout,authenticate


# Create your views here.

def index(request):
    return render(request,'loginapp/index.html')
@login_required    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required    
def special(request):
    return HttpResponseRedirect('Your are logged in Nice')  
def register(request):
    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors) 
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
      
    return render(request,'loginapp/registration.html',{'registered':registered,
                                                            'user_form':user_form,
                                                            'profile_form':profile_form})                    

def user_login(request):
    print('method' + request.method)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print('step1')
        user=authenticate(username=username,password=password)
        if user:
            print('step2')
            if user.is_active:
                login(request,user)
                print('step3')
                return HttpResponseRedirect(reverse(index))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")    
        else:
            print("Some one tried to login and login failed")
            print("UserName:{} password :{}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'loginapp/login.html',{})        



