from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

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




def ok(request):
    return render(request,'shop.html')
def ok1(request):
    return render(request,'index.html')    
def ok2(request):
    return render(request,'sproduct.html')  
def ok3(request):
    return render(request,'cart.html')  
def ok4(request):
    return render(request,'login_page.html') 
def ok5(request):
    return render(request,'signup_page.html') 