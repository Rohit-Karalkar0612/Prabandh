from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('product/',views.Productform,name="product"),
    path('ajax/load_subcat/', views.load_subcat, name='ajax_load_subcat'),
    path('cart/',views.cart,name="cart"),
    path('cartdel/<my_id>',views.cartdel,name="cartdel"),
    path('cartadd/<my_id>',views.cartadd,name="cartadd"),
    path('event/<my_id>',views.Event,name="product"),
    path('Image/<prod_id>',views.Prod_view,name="Prod_view"),
    path("NewImage/",views.NewImage,name="NewImage"),
    path('subcategory/<my_id>/<mysubcat>',views.search_subcat,name="Search subcat"),
    path('Image/',views.load,name="load"),
    path('deleteImage/',views.deleteImage,name="Delete Image"),
    path('subcategory/<str:mysubcat1>', views.search_subcat1, name="Search subcat1"),
    path('search/', views.search_subcat1, name="search"),
    path('check/',views.Check.as_view(),name="check"),
    path('check/create/',views.create_payment,name="create"),
    path('webhook/',views.webhook,name="web"),
    path('success/',views.success.as_view(),name="success"),
]
