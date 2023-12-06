from django.urls import path , include
from .import views
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="apimob",
      default_version='v1',
      description="API  pour un système impliquant la gestion des utilisateurs et le suivi des activités",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
  path('GetUsers', views.api_get_User),
  path('addUser', views.api_add_User),
  path('addAct', views.api_add_Activity),
  path('addUser', views.api_add_User),
  path('delete/<str:email>/',views.delete_user, name='delete_user'),
  path('permission/<str:email>/', views.permission_user, name='disable_user'),
   path('disable/<str:email>/', views.status_user, name='disable_user'),
  path('editUSer/<str:email>/', views.edit_user, name='edit_user'),
  path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
   path('activities/', views.api_get_Activity, name='get_activities'),

   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

  
]
