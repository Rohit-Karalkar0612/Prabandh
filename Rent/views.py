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

def search_match(query,item):
    if query in item.title.lower() or query in item.about.lower() or query in item.category or query in item.subcategory:
        return True
    else:
        return False

def index(request):
    products=Product.objects.all()
    Photos=Photo.objects.all()
    param={
        'product':products,
        'photos':Photos,
    }
    print(products)
    return render(request, 'Rent/home_page.html',param)

def search_subcat(request,my_id,mysubcat):
    if my_id=='1':
        test={
            'Clothes': ['Ethnic','Drum','Gifts','Car',],
            'Car': ['Swift','Audi','Sedan','Mercedes'],
        }
    elif(my_id=='2'):
        test = {
            'Cake': ['Strawberry', 'Pineapple', 'Chocolate', 'Apple', ],
            'Gift': ['Watch', 'Pencil', 'Pen', 'Rubber'],
        }

    category = get_object_or_404(Subcategory, subcategories=mysubcat)
    products = Product.objects.filter(subcategory=category)

    context = {
        'test': test,
        'my_id': my_id,
        'product': products
    }
    return render(request, 'Rent/Weddings.html',context)

def search_subcat1(request):
    query=request.GET.get('search')
    category = get_object_or_404(Subcategory, subcategories='Ethnic')
    products1 = Product.objects.filter(subcategory=category)
    products=[item for item in products1 if search_match(query,item)]
    return render(request, 'Rent/subcstfil.html',{'product':products})

def Event(request,my_id=''):
    # subcat_01=['Ethnic','Drum','Gifts','Car',]
    # subcat_02=['Swift','Audi','Sedan','Mercedes']
    if my_id=='1':
        test={
            'Clothes': ['Ethnic','Drum','Gifts','Car',],
            'Car': ['Swift','Audi','Sedan','Mercedes'],
        }
    elif(my_id=='2'):
        test = {
            'Cake': ['Strawberry', 'Pineapple', 'Chocolate', 'Apple', ],
            'Gift': ['Watch', 'Pencil', 'Pen', 'Rubber'],
        }
    elif(my_id=='3'):
        test = {
            'Clothes': ['Ethnic', 'Drum', 'Gifts', 'Car', ],
            'Car': ['Swift', 'Audi', 'Sedan', 'Mercedes'],
        }

    category = get_object_or_404(Subcategory, subcategories='Ethnic')
    products = Product.objects.filter(subcategory=category)

    context={
        'test':test,
        'my_id':my_id,
        'product':products
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
    request.session['p_id']=prod_id
    ppk=prod_id
    context={
        'Product':Photo.objects.filter(product_photo__id=ppk),
        'pro':Product.objects.get(id=ppk),
        'pform':PhotoForm,
    }
    print(Photo.objects.filter(product_photo__id=ppk))
    print(Product.objects.get(id=ppk))
    if str(request.user)==str(Product.objects.get(id=ppk).seller_of_item):
        print(str(request.user)+" "+str(Product.objects.get(id=ppk).seller_of_item))
        return render(request,'Rent/ProdView.html',context)
    else:
        print(str(request.user)+" "+str(Product.objects.get(id=ppk).seller_of_item))
        return render(request,'Rent/ProdViewCust.html',context)


def load(request):
    ppk=request.session['p_id']
    context={
        'Product':Photo.objects.filter(product_photo__id=ppk),
        'pro':Product.objects.get(id=ppk),
        'pform':PhotoForm,
    }
    return render(request,'Rent/loop.html',context)


def NewImage(request):
    print("lll")
    print(request)
    if request.method=='POST':
        current_url = resolve(request.path_info).url_name
        curr_id=request.POST['blog']
        curr_ph=Product.objects.get(id=curr_id)
        print(request.POST)
        print(request.FILES['photo'])
        print(request.get_full_path())
        form=PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            j=form.save(commit=False)
            j.product_photo=curr_ph
            j.save()
        else:
            print(form.errors)

    return JsonResponse({'bool':True})


def deleteImage(request):
    if request.method=='POST':
        ph_id=request.POST['ph_id']
        p_id=request.POST['p_id']
        i=Product.objects.get(id=p_id)
        i.product_name.filter(id=ph_id).delete()
        
    
    return JsonResponse({'bool':True})

