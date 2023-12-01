from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import User,Activity,Acceleration,Gylocation,Gyroscope
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def api_get_User(request):
    users=User.objects.all()
    json=serializers.serialize("json",users)
    return HttpResponse(json)

require_http_methods(["POST"])
@csrf_exempt
def api_add_User(request):
    try:
        data = json.loads(request.body)
        user = User.create_user(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            dateDeNaissance=data.get('dateDeNaissance'),  # Assurez-vous que le format est correct
            poids=data.get('poids', 0),
            taille=data.get('taille', 0),
            email=data.get('email'),
            motDePasse=data.get('motDePasse')
        )
        return HttpResponse('User created successfully', status=201)
    except Exception as e:
        print(e)
        return HttpResponse(f'Error: {str(e)}', status=500)
    
@require_http_methods(["POST"])
@csrf_exempt
def api_add_Activity(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('email')  
        user = User.objects.get(email=user_id)
        activity = Activity.create_Activity(user=user,etiquette=data.get('etiquette'))

        # Enregistrer les données Gyroscope
        for item in data['gyroscopeData']:
            Gyroscope.create_Gyroscope(x=item['x'], y=item['y'], z=item['z'], activity=activity)

        # Enregistrer les données Acceleration
        for item in data['accelerationData']:
            Acceleration.create_Acceleration(x=item['x'], y=item['y'], z=item['z'], activity=activity)

        # Enregistrer les données Gylocation
        for item in data['gylocationData']:
            Gylocation.create_Gylocation(speed=item['speed'], heading=item['heading'], altitude=item['altitude'], accuracy=item['accuracy'], longitude=item['longitude'], altitudeAccuracy=item['altitudeAccuracy'], latitude=item['latitude'], activity=activity)

        return HttpResponse('Activity created successfully', status=201)

    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
    
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_user(request, email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        return HttpResponse('Utilisateur supprimé avec succès', status=204)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@require_http_methods(["PATCH"])
@csrf_exempt
def disable_user(request, email):
    try:
        user = User.objects.get(email=email)
        user.active = not user.is_active
        user.save()
        return HttpResponse('Utilisateur désactivé avec succès', status=200)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)