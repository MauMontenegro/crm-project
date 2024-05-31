from django.urls import path
from .views import home,customer,products,createOrder,updateOrder,deleteOrder,register,loginPage,logoutUser,userPage,accountSettings
from django.contrib.auth import views as auth_views

from django.contrib import admin

app_name = 'home'

urlpatterns=[
    path("",home,name='home'),
    path("products/",products,name='products'),
    path("customer/<int:pk>/",customer,name='customer'),
    path('user/',userPage,name='user-page'),
    path('create_order/<int:pk>',createOrder,name="create_order"),
    path('update_order/<int:pk>',updateOrder,name="update_order"),
    path('delete_order/<int:pk>',deleteOrder,name='delete_order'),
    path('register/',register,name='register'),
    path('login/',loginPage,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('account/',accountSettings,name='account'),   
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name="password_reset"),   
]