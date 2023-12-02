from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import User,Activity,Acceleration,Gylocation,Gyroscope
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_get_User(request):
    users=User.objects.all()
    json=serializers.serialize("json",users)
    return HttpResponse(json)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        return HttpResponse('Utilisateur supprimé avec succès', status=204)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def disable_user(request, email):
    try:
        user = User.objects.get(email=email)
        user.is_superuser = not user.is_superuser
        user.save()
        return HttpResponse('Utilisateur désactivé avec succès', status=200)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request, email):
    try:
        data = json.loads(request.body)
        user = User.edit_user(
        email=email,
        nom=data.get('nom'),
        prenom=data.get('prenom'),
        dateDeNaissance=data.get('dateDeNaissance'),
        poids=data.get('poids'),
        taille=data.get('taille'),
        motDePasse=data.get('motDePasse')  
        )
        return HttpResponse('Utilisateur désactivé avec succès', status=200)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)