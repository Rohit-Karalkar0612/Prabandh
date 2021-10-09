from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('product/',views.Productform,name="product"),
    path('ajax/load_subcat/', views.load_subcat, name='ajax_load_subcat'),
    path('wedding/',views.Weddings,name="product"),
    path('subcategory/<str:mysubcat>',views.search_subcat,name="Search subcat"),
]
