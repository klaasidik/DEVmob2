from django.urls import path , include
from .import views

urlpatterns = [
  path('GetUsers', views.api_get_User),
  path('addUser', views.api_add_User),
  path('addAct', views.api_add_Activity),
  path('addUser', views.api_add_User),
  path('delete/<str:email>/',views.delete_user, name='delete_user'),
  path('disable/<str:email>/', views.disable_user, name='disable_user'),
  
]
