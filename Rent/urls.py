from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('product/',views.Productform,name="product"),
    path('ajax/load_subcat/', views.load_subcat, name='ajax_load_subcat'),
    path('event/<my_id>',views.Event,name="product"),
    path('Image/<prod_id>',views.Prod_view,name="Prod_view"),
    path("NewImage/",views.NewImage,name="NewImage"),
    path('subcategory/<my_id>/<mysubcat>',views.search_subcat,name="Search subcat"),
    path('Image/',views.load,name="load"),
    path('deleteImage/',views.deleteImage,name="Delete Image"),
]
