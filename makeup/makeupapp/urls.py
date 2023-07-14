from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ok, name='shop'),
    path('index/', views.ok1, name='index'),
    path('sproduct/<int:product_id>/', views.ok2, name='sproduct'),
    path('cart/', views.ok3, name='cart'),
    path('login_page/', views.loginaction, name='login_page'),
    path('login_page/', views.ok4, name='login_page'),
    path('signup_page/', views.signupaction, name='signup_page'),
    path('signup_page/', views.ok5, name='signup_page'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('about/', views.ok6, name='about'),
    path('contact/', views.ok7, name='contact'),
    path('sproduct/', views.ok8, name='sproduct'),
    path('sproduct/try-on/',views.try_on, name='try_on'),




    #path('index/', views.add_to_cart, name='index'),
    #path('cart/', views.add_to_cart, name='cart'),
    #path('cart/', views.cart, name='cart'),
]
