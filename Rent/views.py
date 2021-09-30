
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView
from .models import Product,Photo
from User.models import Seller
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
    if request.method=='POST' :
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            us=request.user
            u = Seller.objects.get(seller=us)
            p = form.save(commit=False)
            p.seller_of_item = u
            p.availability=True
            p.save()
            products = Product.objects.filter(id=(p.pk))
            return render(request, 'Rent/ProdView.html', {'Product': products})
        else:
            return render(request,'Rent/Product.html',{'form':form})
    else:
        form=ProductForm()
    return render(request,'Rent/Product.html',{'form':ProductForm})