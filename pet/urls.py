from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index',views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),


    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('donate', views.donate, name='donate'),
    
    path('verify-otp/<int:user_id>/<str:otp_code>/', views.verify_otp, name='verify_otp'),
]