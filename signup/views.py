from django.shortcuts import render
import pymysql
from django.views.decorators.csrf import csrf_protect

# Replace the following line:
import mysql.connector as sql

# with:
pymysql.install_as_MySQLdb()
import MySQLdb as sql

fn=' '
ln=' '
email=' '
pwd=' '

# Create your views here.
def signupaction(request):
    global nm,email,pwd,bday
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root",passwd="pepperoni@pizzA1",database='makeup')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items(): 
            if key=="fname":
                fn=value
            if key=="lname":
                ln=value 
            if key=="email":
                email=value
            if key=="password":
                pwd=value           
        c="insert into users Values('{}','{}','{}','{}')".format(fn,ln,email,pwd)  
        cursor.execute(c)
        m.commit()


    return render(request,'signup_page.html')    