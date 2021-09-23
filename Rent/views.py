
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView
from .models import Product,Photo
from .forms import ProductForm
# Create your views here.
def index(request):
    products=Product.objects.all()
    Photos=Photo.objects.all()
    param={
        'product':products,
        'photos':Photos,
    }
    return render(request, 'Rent/home_page.html',param)
    
def show(request):
    return render(request, 'Rent/booking.html')
def Productform(request):
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            user=request.session['user']
            u=user.objects.get(username=user)
            p=form.save(commit=False)
            p.Product=u
            p.save()
            return redirect('user')
        else:
            return render(request,'Rent/Product.html',{'form':form})
    else:
        form=ProductForm()
    return render(request,'Rent/Product.html',{'form':ProductForm})