"""Banking_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('home/', views.Home, name='home'),
    
    # User Actions Url
    path('register/', views.Register, name='register'),
    path('userlogin/', views.UserLogin, name='userlogin'),
    path('userDashboard/', views.UserDashboard, name='userDashboard'),
    path('logout/', views.LogOut, name='logout'),
    
    # ManagerLogin Dashboard Actions Url
    
    path('CashierLogin/', views.CashierLogin, name='CashierLogin'),
    path('CashierLoginD/', views.CashierLoginD, name='CashierLoginD'),
    path('ActionAmount/', views.ActionAmount, name='ActionAmount'),
    path('FundsTransfer/', views.FundsTransfer, name='FundsTransfer'),
    
    
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)