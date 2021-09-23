from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterForm,UserForm,SellerForm

# Create your views here.

def Register(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        rform=RegisterForm(request.POST)
        if form.is_valid() and rform.is_valid():
            user=form.save()
            pro=rform.save(commit=False)
            pro.user=user
            request.session['user']=user.username
            pro.save()
            return redirect('seller')
        else:
            print("jajjaja")
            return render(request,'User/register.html',{'user':form,'register':rform})

    else:
        form=UserForm()
    return render(request,'User/register.html',{'user':UserForm,'register':RegisterForm})

def SellerView(request):
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
            return render(request,'User/seller.html',{'form':form})
    else:
        form=SellerForm()
    return render(request,'User/seller.html',{'form':SellerForm})

