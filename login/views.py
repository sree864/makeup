from django.shortcuts import render
import pymysql
import MySQLdb as sql

pymysql.install_as_MySQLdb()

def loginaction(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Establish a connection to the database
        connection = sql.connect(host="localhost", user="root", passwd="pepperoni@pizzA1", database="makeup")
        cursor = connection.cursor()

        # Execute the SQL query to check if the email and password match
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        # If no result is found, redirect to index.html
        if not result:
            return render(request, "index.html")
        else:
            return render(request, "shop.html")

    return render(request, "login_page.html")
