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
    """
    Récupère et retourne tous les utilisateurs.

    Cette vue retourne une liste de tous les utilisateurs enregistrés dans le système. 
    Elle nécessite une authentification et que l'utilisateur soit authentifié.
    """
    users=User.objects.all()
    json=serializers.serialize("json",users)
    return HttpResponse(json)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_get_Activity(request,email=None):
    """
    Récupère et retourne les activités d'un utilisateur spécifique ou une liste vide si aucun email n'est spécifié.

    Cette vue retourne une liste des activités pour un utilisateur spécifié par son email. 
    Si aucun email n'est fourni, une liste vide est retournée. Elle nécessite une authentification 
    et que l'utilisateur soit authentifié.
    """

    if email:
        # Récupérer les activités pour l'utilisateur spécifié
        activities = Activity.objects.filter(user__email=email)
    else:
        # Retourner une liste vide si aucun email n'est spécifié
        activities = Activity.objects.none()
    
    json_data = serializers.serialize("json", activities)
    return HttpResponse(json_data)



@api_view(['POST'])
@csrf_exempt
def api_add_User(request):
    """
    Ajoute un nouvel utilisateur au système.

    Ce endpoint permet la création d'un nouvel utilisateur. Les champs nécessaires pour 
    la création d'un utilisateur incluent nom, prénom, date de naissance, poids, taille, 
    email et mot de passe. La protection CSRF est désactivée pour cet endpoint.
    """
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
    """
    Ajoute une nouvelle activité pour un utilisateur spécifique.

    Les données nécessaires pour la création d'une activité incluent l'identifiant de l'utilisateur 
    (email) et des détails sur l'activité (étiquette, données de gyroscope, données d'accélération, 
    et données de localisation). L'utilisateur doit être authentifié pour accéder à cet endpoint.
    """
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
    """
    Supprime un utilisateur spécifié par son email.

    Ce endpoint supprime l'utilisateur correspondant à l'email fourni. Il requiert 
    l'authentification et des permissions d'utilisateur authentifié.
    """
    try:
        user = User.objects.get(email=email)
        user.delete()
        return HttpResponse('Utilisateur supprimé avec succès', status=204)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def permission_user(request, email):
    """
    Active ou désactive le permission d'utilisateur superuser basé sur son email.

    Ce endpoint inverse le statut de superuser pour l'utilisateur spécifié. 
    L'opération nécessite que l'utilisateur appelant soit authentifié et disposant des permissions nécessaires.
    """
    try:
        user = User.objects.get(email=email)
        user.is_superuser = not user.is_superuser
        user.save()
        return HttpResponse('Utilisateur permission changé avec succès', status=200)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def status_user(request, email):
    """
    Active ou désactive le permission d'utilisateur superuser basé sur son email.

    Ce endpoint inverse le statut de superuser pour l'utilisateur spécifié. 
    L'opération nécessite que l'utilisateur appelant soit authentifié et disposant des permissions nécessaires.
    """
    try:
        user = User.objects.get(email=email)
        user.is_active = not user.is_active
        user.save()
        return HttpResponse('Utilisateur désactivé avec succès', status=200)
    except User.DoesNotExist:
        return HttpResponse('Utilisateur non trouvé', status=404)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request, email):
    """
    Modifie les informations d'un utilisateur spécifié par son email.

    Permet la mise à jour des détails de l'utilisateur, y compris nom, prénom, date de naissance, 
    poids, taille et mot de passe. L'utilisateur doit être authentifié pour effectuer cette opération.
    """
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