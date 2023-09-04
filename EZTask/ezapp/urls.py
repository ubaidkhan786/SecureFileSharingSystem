from django.urls import path
from .views import userLogin,userLogout,registerUser,verify_email

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('verify/',verify_email,name='verify'),
]