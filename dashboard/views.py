from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from firebase_admin import auth
from activityTracker.models import User
from django.db.models import Count
from .forms import CustomUserCreationForm
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

import requests
import firebase_admin


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login')  # Redirection après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Créer ou récupérer un token pour l'utilisateur
            token, created = Token.objects.get_or_create(user=user)
            
            response = redirect('/index')
            response.set_cookie('auth_token', token.key)  # stocker le token dans un cookie
            # ou
            request.session['auth_token'] = token.key  # stocker le token dans la session
            return response
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def google_login(request):
    # Ici, vous récupérerez les informations de l'utilisateur
    if not request.user.is_authenticated:
        return redirect('social:begin', backend='google-oauth2')
    else:
        # L'utilisateur est déjà authentifié, vous pouvez le rediriger
        return redirect('/index')  # Remplacez 'home' par votre URL de redirection
    
def get_or_create_user(decoded_token):
    uid = decoded_token['uid']
    email = decoded_token.get('email')
    name = decoded_token.get('name')

    user, created = User.objects.get_or_create(username=uid, defaults={'email': email})
    return user

@csrf_exempt
def custom_login_view(request):
    token = request.POST.get('token')
  
        # Vérification du token Firebase
    decoded_token = auth.verify_id_token(token)
    print(decoded_token)




def is_admin(user):
    return user.is_staff or user.is_superuser



def index(request):
    if request.user.is_staff or request.user.is_superuser:
       users= User.objects.annotate(nb_activ=Count('activity')) 
       return render(request, 'index.html',{'users':users})
    else:
        return redirect('not_admin') 
    
def not_admin(request):
    logout(request)
    return render(request, 'not_admin.html')

def logout_view(request):
    logout(request)
    response = redirect('/login')
    response.delete_cookie('auth_token')  # Supprimez le cookie si vous stockez le token dans un cookie
    return response