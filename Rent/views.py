from django.shortcuts import render
from .models import Product,Photo
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