from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ok, name='shop'),
    path('index/', views.ok1, name='index'),
    path('sproduct/', views.ok2, name='sproduct'),
    path('cart/', views.ok3, name='cart'),
]
