from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from .models import Product,Photo,Subcategory,Category
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
def load_subcat(request):
    print('Hello')
    category_id = request.GET.get('CategoryId')
    subcategory = Subcategory.objects.filter(Categories=category_id).all()
    print(subcategory)
    return render(request, 'Rent/subcat.html', {'subcat': subcategory})
def show(request):
    return render(request, 'Rent/booking.html')
def Productform(request):
    if request.method=='POST' :
        form=ProductForm(request.POST,request.FILES)
        print(form)
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
            print(form.errors)
            return render(request,'Rent/Product.html',{'form':form})
    else:
        form=ProductForm()
    return render(request,'Rent/Product.html',{'form':ProductForm})