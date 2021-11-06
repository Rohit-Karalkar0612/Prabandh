from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterForm,UserForm,SellerForm
from User.models import Profile
from .models import Seller

# Create your views here.

def Register(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        rform=RegisterForm(request.POST)
        if form.is_valid() and rform.is_valid():

            user=form.save()
            pro=rform.save(commit=False)
            isSeller=rform.cleaned_data['seller']
            print(isSeller)
            pro.user=user
            request.session['user']=user.username
            pro.save()
            if isSeller:
                return redirect('seller')
            else:
                return redirect('home')
        else:
            print(form.errors)
            return render(request,'User/register.html',{'user':form,'register':rform})

    else:
        # print(form.errors)
        form=UserForm()
    return render(request,'User/register.html',{'user':UserForm,'register':RegisterForm})

def SellerView(request):
    # if Seller.objects.filter(seller=request.user).count()==0 or Seller.objects.filter(seller=User.objects.get(username=request.session['user'])).count()==0:
        if request.method=='POST':
            form=SellerForm(request.POST)
            if form.is_valid():
                user=request.session['user']
                u=User.objects.get(username=user)
                p=form.save(commit=False)
                p.seller=u
                p.save()
                return redirect('register')
            else:
                return render(request,'User/seller.html',{'user':form})
        else:
            form=SellerForm()
        return render(request,'User/seller.html',{'user':SellerForm})

def profile(request):
    allProfile = Profile.objects.filter(user=request.user)
    param_profile = {
        'Profile' : allProfile
    }
    return render(request,'User/profile.html',param_profile)