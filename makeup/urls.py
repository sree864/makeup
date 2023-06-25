from django.contrib import admin
from django.urls import path
from signup.views import signupaction
from login.views import loginaction
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup_page/', signupaction),
    path('login_page/', loginaction),
    path('', signupaction),
    path('', loginaction),  # Add this line to handle the empty path
]