from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from firebase_admin import auth
from activityTracker.models import User
from django.db.models import Count
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login')  # Redirection après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/index')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def google_login(request):
    print(request.user)
    # Ici, vous récupérerez les informations de l'utilisateur
    if not request.user.is_authenticated:
        return redirect('social:begin', backend='google-oauth2')
    else:
        # L'utilisateur est déjà authentifié, vous pouvez le rediriger
        return redirect('/index')  # Remplacez 'home' par votre URL de redirection


def is_admin(user):
    return user.is_staff or user.is_superuser



@login_required
def index(request):
    if request.user.is_staff or request.user.is_superuser:
       users= User.objects.annotate(nb_activ=Count('activity')) 
       return render(request, 'index.html',{'users':users})
    else:
        return redirect('not_admin') 
    
def not_admin(request):
    logout(request)
    return render(request, 'not_admin.html')