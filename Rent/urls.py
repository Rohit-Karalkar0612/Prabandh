from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('product/',views.Productform,name="product"),
    path('ajax/load_subcat/', views.load_subcat, name='ajax_load_subcat'),
    path('cart/',views.cart,name="cart"),
    path('noti/',views.Issue,name="issue"),
    path('update/<my_id>',views.update,name="update"),
    path('issue/<my_id>',views.issueform,name="issueform"),
    path('rentedProduct', views.rentprod, name="rentprod"),
    path('Onrent', views.putrent, name="putrent"),
    path('cartdel/<my_id>',views.cartdel,name="cartdel"),
    path('cartadd/<my_id>',views.cartadd,name="cartadd"),
    path('Image/<prod_id>',views.Prod_view,name="Prod_view"),
    path("NewImage/",views.NewImage,name="NewImage"),
    path('event/<my_id>/<mysubcat>/<my_id1>',views.search_subcat,name="Search subcat"),
    path('Image/',views.load,name="load"),
    path('deleteImage/',views.deleteImage,name="Delete Image"),
    path('subcategory/<str:mysubcat1>/', views.search_subcat1, name="Search subcat1"),
    path('search/<my_id>', views.search_subcat1, name="search"),
    path('check/',views.Check.as_view(),name="check"),
    path('check/create/',views.create_payment,name="create"),
    path('webhook/',views.webhook,name="web"),
    path('success/',views.success.as_view(),name="success"),
    path('details/',views.RentAmt,name="detail"),
    path('booking/',views.rentprod,name="booking"),
    path('putrent/',views.putrent,name="putrent"),
    path('rate/<my_id>',views.rate,name="rate")
]
