"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from .import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('google-login/', views.google_login, name='google_login'),
    path('apimob/', include('activityTracker.urls')),
    path('index/', views.index, name='index'),
    path('not-admin/', views.not_admin, name='not_admin'),
    path('logout/', views.logout_view, name='logout'),
    path('login_firebase/', views.custom_login_view, name='login_firebase'),

]

