from django.shortcuts import render
from django.http import HttpResponse

def ok(request):
    return render(request,'shop.html')
def ok1(request):
    return render(request,'index.html')    
def ok2(request):
    return render(request,'sproduct.html')  
def ok3(request):
    return render(request,'cart.html')  