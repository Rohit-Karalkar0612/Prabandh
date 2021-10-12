from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from .models import Product,Photo,Subcategory,Category,Photo
from User.models import Seller
from .forms import ProductForm,PhotoForm
from django.urls import reverse,resolve
from urllib.parse import urlencode
# Create your views here.
def index(request):
    products=Product.objects.all()
    Photos=Photo.objects.all()
    param={
        'product':products,
        'photos':Photos,
    }
    print(products)
    return render(request, 'Rent/home_page.html',param)

def search_subcat(request,mysubcat):
    category = get_object_or_404(Subcategory, subcategories=mysubcat)
    products = Product.objects.filter(subcategory=category)
    return render(request, 'Rent/subcstfil.html',{'product':products})

def Weddings(request,my_id):
    # subcat_01=['Ethnic','Drum','Gifts','Car',]
    # subcat_02=['Swift','Audi','Sedan','Mercedes']
    if my_id==1:
        test={
            'Clothes': ['Ethnic','Drum','Gifts','Car',],
            'Car': ['Swift','Audi','Sedan','Mercedes'],
        }
    elif(my_id==2):
        test = {
            'Clothes': ['Ethnic', 'Drum', 'Gifts', 'Car', ],
            'Car': ['Swift', 'Audi', 'Sedan', 'Mercedes'],
        }
    elif(my_id==3):
        test = {
            'Clothes': ['Ethnic', 'Drum', 'Gifts', 'Car', ],
            'Car': ['Swift', 'Audi', 'Sedan', 'Mercedes'],
        }
    test = {
        'Clothes': ['Ethnic', 'Drum', 'Gifts', 'Car', ],
        'Car': ['Swift', 'Audi', 'Sedan', 'Mercedes'],
    }
    context={
        'test':test
    }
    return render(request,'Rent/Weddings.html',context)
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
        service=['DJ','Banquet Hall','Car']
        if form.is_valid():
            us=request.user
            u = Seller.objects.get(seller=us)
            p = form.save(commit=False)
            p.seller_of_item = u
            p_img=p.image_of_product
            print(p_img)
            if 'p.subcategory' in service:
                p.availability=False
            else:
                p.availability = True
            p.save()
            products = Product.objects.get(id=(p.pk))
            ph=Photo(photo=p_img,product_photo=products)
            request.session['p_id']=p.pk
            ph.save()
            # base=reverse('Prod_view')
            # query=urlencode({'prod_id':p.pk})
            # url='{}?{}'.format(base,query)
            return redirect('Prod_view',p.pk)
        else:
            print(form.errors)
            return render(request,'Rent/Product.html',{'form':form})
    else:
        form=ProductForm()
    return render(request,'Rent/Product.html',{'form':ProductForm})


def Prod_view(request,prod_id):
    # print(pk)
    ppk=prod_id
    context={
        'Product':Photo.objects.filter(product_photo__id=ppk),
        'pro':Product.objects.get(id=ppk),
        'pform':PhotoForm,
    }
    return render(request,'Rent/ProdView.html',context)


def load(request):
    ppk=request.session['p_id']
    context={
        'Product':Photo.objects.filter(product_photo__id=ppk),
        'pro':Product.objects.get(id=ppk),
        'pform':PhotoForm,
    }
    return render(request,'Rent/loop.html',context)


def AddImage(request):
    if request.method=='POST':
        current_url = resolve(request.path_info).url_name
        print(request.POST)
        print(request.get_full_path())
        # if 'djj' in request.POST:
        #     print("KDSKSk")
        t=request.POST.get('djj')
        # # t1=request.FILES['djj']
        form=PhotoForm(t)
        # print(t)
        if form.is_valid():
            form.save()
            return JsonResponse({'bool':True})
        else:
            print(form.errors)

    return JsonResponse({'bool':True})