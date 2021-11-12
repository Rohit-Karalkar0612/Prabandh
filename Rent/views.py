from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Min,Max
from django.views.generic import CreateView,TemplateView
from .models import Product,Photo,Subcategory,Category,Photo,Cart,Rent_Amount,Ratings,Issues
from User.models import Seller,User,Profile
from .forms import ProductForm,PhotoForm,RentForm,IssueForm,RentForm
from django.urls import reverse,resolve
from urllib.parse import urlencode
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date,timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY





def cart(request):
    us = request.user
    Cartobj = (Cart.objects.filter(user=us)).values('product_id')
    print(Cartobj)
    prod = []
    j = 0
    for i in Cartobj:
        j = j + 1
    print(j)
    for i in range(0, j):
        prod = prod + list(Cartobj[i].values())
    print(prod)
    sum = 0
    products = Product.objects.filter(id__in=prod)
    for i in products:
        sum = sum + i.deposit

    request.session['total']=sum
    param = {
        'product': products,
        'sum': sum,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    print(products)
    return render(request, 'Rent/subcstfil.html', param)


def cart(request):

    if request.method=='POST':
        my_items = Cart.objects.filter(user=request.user)
        print(my_items)
        total = 0
        d=date.today()
        s=d.strftime("%Y-%m-%d")
        r=Rent_Amount.objects.all()
        listw=[]
        for y in r:
            listw.append(y.related_product)
        
        print(listw)
        print(s)
        for p in my_items:
            if p.product_id not in listw:
                print(p)
                form=RentForm(request.POST)
                unsave=form.save(commit=False)
                u=form.cleaned_data['expected']
                unsave.related_product=p.product_id
                unsave.customer_of_item=request.user
                print(request.session['total'])
                unsave.payment=request.session['total']
                unsave.delivered_date=s
                unsave.sent_date=u
                unsave.save()
                print("ll")              

        
        return redirect('check')





    user = request.user
    Cartobj=(Cart.objects.filter(user=user)).values('product_id')
    print(Cartobj)
    prod=[]
    j=0
    for i in Cartobj:
        j=j+1
    print(j)
    for i in range(0, j):
        prod=prod+list(Cartobj[i].values())
    print(prod)
    sum=0
    products = Product.objects.filter(id__in=prod)
    
    for i in products:
        sum=sum+i.deposit

    request.session['total']=sum

    u = User.objects.get(username=user)
    isSeller=Profile.objects.get(user=u).seller

    print(isSeller)
    param = {
        'product': products,
        'sum':sum,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        'us':isSeller,
        'form':RentForm
    }
    print(products)
    return render(request, 'User/cart.html', param)


def rentprod(request):
    us = request.user
    RentPr = Rent_Amount.objects.filter(customer_of_item=us).values('related_product')
    RentProd=RentPr.values('related_product')

    print(RentProd)
    prod = []
    j = 0
    for i in RentProd:
        j = j + 1
    print(j)
    for i in range(0, j):
        prod = prod + list(RentProd[i].values())
    print(prod)
    sum = 0
    products = Product.objects.filter(id__in=prod)
    param = {
        'product': products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'Rent/subcstfil.html', param)

def putrent(request):
    us = request.user
    u = Seller.objects.get(seller=us)
    products = Product.objects.filter(seller_of_item=u)
    param = {
        'product': products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'Rent/subcstfil.html', param)


def cartadd(request, my_id):
    us = request.user
    prod = Product.objects.get(id=my_id)
    cart1=Cart.objects.filter(user=us, product_id=prod).exists()
    if cart1!=True:
        b = Cart(user=us, product_id=prod)
        b.save()
    return redirect('cart')


def cartdel(request, my_id):
    Cart.objects.filter(product_id=my_id).delete()
    return redirect('cart')


def search_match(query, item):
    if query in item.title.lower() or query in item.about.lower():
        return True
    else:
        return False


def index(request):
    k=0
    if request.user.is_authenticated:
        us = request.user
        k = 0
        sell = Seller.objects.filter(seller=us).exists()
        if sell == True:
            u = Seller.objects.get(seller=us)
            product = (Product.objects.filter(seller_of_item=u)).values('id')
            print(product)
            prod = []
            j = 0
            for i in product:
               j = j + 1
            print(j)
            for i in range(0, j):
                prod = prod + list(product[i].values())
            print(prod)
            print("Hello")
            rentamount = Rent_Amount.objects.filter(related_product_id__in=prod, satisfaction=False)
            print(rentamount)
            print("Hello1")
            product1 = {}
            for r in rentamount:
                prod = Issues.objects.filter(complain_against=r.related_product, complainer=us).exists()
                if r.delivered_date <= date.today() and prod!=True:
                    print(r.related_product_id)
                    k = k + 1
                    product1 = Product.objects.filter(id=r.related_product_id)

        product2 = {}
        rentamount = Rent_Amount.objects.filter(customer_of_item=us)
        for r in rentamount:
            prod = Ratings.objects.filter(rating_for_product=r.related_product, rating_by=us).exists()
            if r.sent_date <= date.today() and prod != True:
                product2 = Product.objects.filter(id=r.related_product_id)
                k = k + 1
        product3 = {}
        rentamount = Rent_Amount.objects.filter(customer_of_item=us)
        print(rentamount)
        for r in rentamount:
            print(r.delivered_date)
            print(date.today() + timedelta(days=1))
            if r.sent_date == (date.today() + timedelta(days=1)):
                print(date.today() + timedelta(days=1))
                product3 = Product.objects.filter(id=r.related_product_id)
    param = {
        'k':k,
    }
    return render(request, 'Rent/home_page.html', param)


def search_subcat(request, my_id, mysubcat,my_id1):
    if my_id == '1':
        test = {
            'Clothes': ['Ethnic', 'Western', 'Jackets', 'Denims'],
            'Car': ['Swift', 'Audi', 'Sedan', 'Mercedes'],
        }
    elif (my_id == '2'):
        test = {
            'Formals': ['Ethnicity', 'Sweatshirts', 'Jacket', 'Hoodies', ],
            'Decorations': ['Posters', 'Balloons', 'Streamers', 'Party Hats'],
        }
    elif (my_id == '3'):
        test = {
            'Essentials-1': ['Flowers', 'Chandeliers', 'Paper decor', 'Fairy Lights', ],
            'Essentials-2': ['LED Diyas', 'Electric Lamps', 'Photo Frames', 'Wall Decor'],
        }
    category = get_object_or_404(Subcategory, subcategories=mysubcat)
    products = Product.objects.filter(subcategory=category,availability=True)
    if my_id1 == '2':
        min2 = ''
        min1 = request.GET.get('min-value')
        for i in min1:
            if i == ',':
                pass
            else:
                min2 = min2 + i
        min = int(min2)
        max2 = ''
        max1 = request.GET.get('max-value')
        for i in max1:
            if i == ',':
                pass
            else:
                max2 = max2 + i
        max = int(max2)
        print(min)
        print(max)
        products = Product.objects.filter(subcategory=category, rental_price__range=(min, max),availability=True)
    min_price = products.aggregate(Min('rental_price'))
    max_price = products.aggregate(Max('rental_price'))
    price = {**min_price, **max_price}
    print(price)
    print(min_price)
    context = {
        'test': test,
        'my_id': my_id,
        'product': products,
        'price': price,
        'mysubcat':mysubcat,

    }
    return render(request, 'Rent/Weddings.html', context)


def search_subcat1(request,my_id=''):
    query = request.GET.get('search')
    products=Product.objects.filter(availability=True)
    if my_id == '2':
        min2 = ''
        min1 = request.GET.get('min-value')
        for i in min1:
            if i == ',':
                pass
            else:
                min2 = min2 + i
        min = int(min2)
        max2 = ''
        max1 = request.GET.get('max-value')
        for i in max1:
            if i == ',':
                pass
            else:
                max2 = max2 + i
        max = int(max2)
        print(min)
        print(max)
        products = Product.objects.filter(rental_price__range=(min, max),availability=True)
    products = [item for item in products if search_match(query, item)]
    return render(request, 'Rent/prod.html', {'products': products})


def Event(request, my_id='', my_id1='0'):
    # subcat_01=['Ethnic','Drum','Gifts','Car',]
    # subcat_02=['Swift','Audi','Sedan','Mercedes']
    if my_id=='1':
        test={
            'Clothes': ['Ethnic','Western','Jackets','Denims'],
            'Car': ['Swift','Audi','Sedan','Mercedes'],
        }
    elif (my_id == '2'):
        test = {
            'Formals': ['Ethnicity', 'Sweatshirts', 'Jacket', 'Hoodies', ],
            'Decorations': ['Posters', 'Balloons', 'Streamers', 'Party Hats'],
        }
    elif (my_id == '3'):
        test = {
            'Essentials-1': ['Flowers', 'Chandeliers', 'Paper decor', 'Fairy Lights', ],
            'Essentials-2': ['LED Diyas', 'Electric Lamps', 'Photo Frames', 'Wall Decor'],
        }

    temp_str = [elem[0] for elem in test.values()]
    print("Hello")
    print(temp_str[0])
    print("Hello1")
    category = get_object_or_404(Subcategory, subcategories= temp_str[0])
    products = Product.objects.filter(subcategory=category)
    if my_id1 == '2':
        min2 = ''
        min1 = request.GET.get('min-value')
        for i in min1:
            if i == ',':
                pass
            else:
                min2 = min2 + i
        min = int(min2)
        max2 = ''
        max1 = request.GET.get('max-value')
        for i in max1:
            if i == ',':
                pass
            else:
                max2 = max2 + i
        max = int(max2)
        print(min)
        print(max)
        products = Product.objects.filter(subcategory=category, rental_price__range=(min, max))
    min_price = products.aggregate(Min('rental_price'))
    max_price = products.aggregate(Max('rental_price'))
    price = {**min_price, **max_price}
    print(price)
    print(min_price)
    context = {
        'test': test,
        'my_id': my_id,
        'product': products,
        'price': price,

    }

    return render(request, 'Rent/Weddings.html', context)


def load_subcat(request):
    print('Hello')
    category_id = request.GET.get('CategoryId')
    subcategory = Subcategory.objects.filter(Categories=category_id).all()
    print(subcategory)
    return render(request, 'Rent/subcat.html', {'subcat': subcategory})


def show(request):
    return render(request, 'Rent/booking.html')


def Productform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        service = ['DJ', 'Banquet Hall', 'Car']
        if form.is_valid():
            us = request.user
            u = Seller.objects.get(seller=us)
            p = form.save(commit=False)
            p.seller_of_item = u
            p_img = p.image_of_product
            print(p_img)
            if 'p.subcategory' in service:
                p.availability = False
            else:
                p.availability = True
            p.save()
            products = Product.objects.get(id=(p.pk))
            ph = Photo(photo=p_img, product_photo=products)
            request.session['p_id'] = p.pk
            ph.save()
            # base=reverse('Prod_view')
            # query=urlencode({'prod_id':p.pk})
            # url='{}?{}'.format(base,query)
            return redirect('Prod_view', p.pk)
        else:
            print(form.errors)
            return render(request, 'Rent/Product.html', {'form': form})
    else:
        form = ProductForm()
    return render(request, 'Rent/Product.html', {'form': ProductForm})


def Prod_view(request, prod_id):
    # print(pk)
    request.session['p_id']=prod_id
    ppk=prod_id
    obj = Ratings.objects.filter(rating_for_product = Product.objects.get(id=ppk))
    context={
        'Product':Photo.objects.filter(product_photo__id=ppk),
        'pro':Product.objects.get(id=ppk),
        'pform':PhotoForm,
        'object': obj
    }
    print(Photo.objects.filter(product_photo__id=ppk))
    print(Product.objects.get(id=ppk))
    if str(request.user) == str(Product.objects.get(id=ppk).seller_of_item):
        print(str(request.user) + " " + str(Product.objects.get(id=ppk).seller_of_item))
        return render(request, 'Rent/ProdView.html', context)
    else:
        print(str(request.user) + " " + str(Product.objects.get(id=ppk).seller_of_item))
        return render(request, 'Rent/ProdViewCust.html', context)


def load(request):
    ppk = request.session['p_id']
    context = {
        'Product': Photo.objects.filter(product_photo__id=ppk),
        'pro': Product.objects.get(id=ppk),
        'pform': PhotoForm,
    }
    return render(request, 'Rent/loop.html', context)


def NewImage(request):
    print("lll")
    print(request)
    if request.method == 'POST':
        current_url = resolve(request.path_info).url_name
        curr_id = request.POST['blog']
        curr_ph = Product.objects.get(id=curr_id)
        print(request.POST)
        print(request.FILES['photo'])
        print(request.get_full_path())
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(commit=False)
            j.product_photo = curr_ph
            j.save()
        else:
            print(form.errors)

    return JsonResponse({'bool': True})

def Issue(request):
    us = request.user
    i=0


    product1 = {}
    sell=Seller.objects.filter(seller=us).exists()
    if sell==True:
        u = Seller.objects.get(seller=us)
        product=(Product.objects.filter(seller_of_item=u)).values('id')
        print(product)
        prod = []
        j = 0
        for i in product:
            j = j + 1
        print(j)
        for i in range(0, j):
            prod = prod + list(product[i].values())
        print(prod)
        print("Hello")
        rentamount=Rent_Amount.objects.filter(related_product_id__in=prod,satisfaction=False)
        print(rentamount)
        print("Hello1")
        for r in rentamount:
            prod = Issues.objects.filter(complain_against=r.related_product, complainer=us).exists()
            if r.delivered_date<= date.today() and prod!=True:
                print(r.related_product_id)
                i=i+1
                product1=Product.objects.filter(id=r.related_product_id)

    product2={}
    rentamount = Rent_Amount.objects.filter(customer_of_item=us)
    for r in rentamount:
        prod = Ratings.objects.filter(rating_for_product=r.related_product,rating_by=us).exists()
        if r.sent_date <= date.today() and prod!=True:
            product2=Product.objects.filter(id=r.related_product_id)
            i=i+1
    product3 = {}
    rentamount = Rent_Amount.objects.filter(customer_of_item=us)
    print(rentamount)
    for r in rentamount:
        print(r.delivered_date)
        print(date.today()+timedelta(days=1))
        if r.sent_date == (date.today()+timedelta(days=1)):
            print(date.today()+timedelta(days=1))
            i=i+1
            product3=Product.objects.filter(id=r.related_product_id)
    context={
        'product':product1,
        'products':product2,
        'products1':product3,
        'i': i,

    }
    return render(request, 'Rent/subcstfil.html', context)

def update(request,my_id):
    Rent_Amount.objects.filter(related_product_id=my_id).update(satisfaction=True)
    return redirect('/')

def deleteImage(request):
    if request.method == 'POST':
        ph_id = request.POST['ph_id']
        p_id = request.POST['p_id']
        i = Product.objects.get(id=p_id)
        i.product_name.filter(id=ph_id).delete()

    return JsonResponse({'bool': True})


def create_payment(request):
    if request.method == 'POST':
        my_items = Cart.objects.filter(user=request.user)
        total = 0
        for p in my_items:
            total += (p.product_id.deposit)

        print(total)
        # data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=total * 100,
            currency='INR',
            metadata={
                'id':request.user.id
            },
            payment_method_types=[
                'card',
            ],
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })


class Check(TemplateView):
    template_name = "Rent/checkout.html"


    def get_context_data(self, **kwargs):
        my_items = Cart.objects.filter(user=self.request.user)
        total = 0
        for p in my_items:
            u=(p.product_id.rented_product.expected-datetime.strptime(date.today().strftime("%Y-%m-%d"),"%Y-%m-%d").date()).days
            print(u)
            print("hadsgdf")
            u=u*p.product_id.rental_price
            total =total+u+ (p.product_id.deposit)

        context = super().get_context_data(**kwargs)
        context["total"] = total
        return context


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        carti=session['metadata']['id']
        c=Cart.objects.filter(user=User.objects.get(id=carti))
        for item in c:
            p=Product.objects.filter(id=item.product_id.id)
            p.update(availability=False)

        

        # print(session)

    # Passed signature verification
    return HttpResponse(status=200)


class success(TemplateView):
    template_name="Rent/success.html"


def RentAmt(request):
    return render(request,'Rent/details.html',{'form':RentForm})



def rentprod(request):
    user = request.user
    RentProd=Rent_Amount.objects.filter(customer_of_item=user).values('related_product')
    # print(RentProd)
    prod = []
    j = 0
    for i in RentProd:
        j = j + 1
    # print(j)
    for i in range(0, j):
        prod = prod + list(RentProd[i].values())
    # print(prod)
    sum = 0
    products = Product.objects.filter(id__in=prod)
    u = User.objects.get(username=user)
    isSeller=Profile.objects.get(user=u).seller
    print(isSeller)
    param = {
        'product': products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        'us':isSeller
    }
    return render(request, 'User/booking.html', param)

def putrent(request):
    user = request.user
    u = Seller.objects.get(seller=user)
    print(user)
    us = User.objects.get(username=user)
    isSeller=Profile.objects.get(user=us).seller
    print(isSeller)
    products = Product.objects.filter(seller_of_item=u)
    param_putrent = {
        'product': products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        'us':isSeller
    }

    return render(request, 'User/add_rent.html', param_putrent)

def rate(request,my_id):
    us = request.user
    product = Product.objects.filter(id = my_id)
    for j in product:
        j = j
    print(us)
    print(j)
    if request.method=='POST':
        rating = request.POST['rating']
        review = request.POST['review']
        data = Ratings(rating_for_product= j,rating_by= us,rating=rating,review=review)
        data.save()
        return redirect('/')

def issueform(request,my_id):
    us = request.user
    product = Product.objects.filter(id = my_id)
    for j in product:
        j = j
    print(us)
    print(j)
    if request.method=='POST':
        issue = request.POST['issue']
        data = Issues(complainer=us,complain_against=j,issue=issue,resolved=False)
        data.save()
        return redirect('/')