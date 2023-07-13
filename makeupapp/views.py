from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed

#signup page variables
fn=''
ln=''
em=''
pwd=''

def signupaction(request):
    global nm,em,pwd,bday
    if request.method=="POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="pepperoni@pizzA1", database="makeup")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items(): 
            if key=="fname":
                fn=value
            if key=="lname":
                ln=value 
            if key=="email":
                em=value
            if key=="password":
                pwd=value           
        c = "INSERT INTO users (firstname, lastname, emailid, password) VALUES ('{}', '{}', '{}', '{}')".format(fn, ln, em, pwd)
        cursor.execute(c)
        m.commit()


    return render(request,'signup_page.html')  

def loginaction(request):
    global em,pwd
    if request.method=="POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="pepperoni@pizzA1", database="makeup")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items(): 
            if key=="email":
                em=value
            if key=="password":
                pwd=value           
        c = "SELECT * from users where emailid='{}' and password='{}'".format(em, pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            return render(request,'error.html')
        else:
            return render(request,'index.html')
    return render(request,'login_page.html')  

def add_to_cart(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        
        # Implement your logic to add the product to the cart
        # Store the product information in the cart database or session
        
        return redirect('cart')  # Redirect to the cart page after adding the product

    return HttpResponseNotAllowed(['POST'])

def cart(request):
    # Retrieve cart items from the database or session
    cart_items = [
        {'product_name': 'Mac Lipstick shade Red Gloss', 'price': 11.8, 'quantity': 1, 'subtotal': 11.8},
        # Add more cart items here
    ]
    
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)


def ok(request):
    return render(request,'shop.html')
def ok1(request):
    return render(request,'index.html')    
def ok2(request, product_id):
    # Retrieve the product information based on the product_id from your database
    # You can use the product_id to query the database and get the corresponding name and price

    lipstick_name = "Lipstick Name"  # Replace with the retrieved product name
    lipstick_price = 800  # Replace with the retrieved product price

    context = {
        'lipstick_name': lipstick_name,
        'lipstick_price': lipstick_price,
    }

    return render(request, 'sproduct.html', context)

def ok3(request):
    return render(request,'cart.html')  
def ok4(request):
    return render(request,'login_page.html') 
def ok5(request):
    return render(request,'signup_page.html') 
def ok6(request):
    return render(request,'about.html') 
def ok7(request):
    return render(request,'contact.html') 
def ok8(request):
    return render(request,'sproduct.html') 




def sproduct(request):
    image = request.GET.get('image')
    product_encoded = request.GET.get('product')

    # Decode the product JSON object
    import json
    product = json.loads(product_encoded)

    product_name = product.get('name')
    product_price = product.get('price')

    # You can use the retrieved product name and price in your view logic

    # For demonstration purposes, let's return a response with the retrieved data
    return HttpResponse(f"Image: {image}<br>Product Name: {product_name}<br>Product Price: {product_price}")
