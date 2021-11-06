from django.urls import path,include
from .views import Register
from User import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',user_views.Register,name="register"),
    path('seller/',user_views.SellerView,name="seller"),
    path('profile/',user_views.profile,name="profile"),
    path('login/',auth_views.LoginView.as_view(template_name='User\login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='User\logout.html'),name='logout'),
]