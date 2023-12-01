from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    nom=models.CharField(max_length=200)
    prenom=models.CharField(max_length=200)
    dateDeNaissance=models.DateField(default=timezone.now)
    poids=models.FloatField(default=0)
    taille=models.FloatField(default=0)
    email=models.EmailField(unique=True, primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    @classmethod
    def create_user(cls, nom, prenom, dateDeNaissance, poids, taille, email, motDePasse):
        user = cls(nom=nom, prenom=prenom, dateDeNaissance=dateDeNaissance,
                   poids=poids, taille=taille, email=email)
        user.set_password(motDePasse)
        user.save()
        return user

# Create your models here.
class Activity(models.Model):
    dateCreation=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    etiquette=models.CharField(max_length=200)
    @classmethod
    def create_Activity(cls,user,etiquette ):
        activity = cls(user=user,etiquette=etiquette)
        # Ajoutez ici la logique pour hacher le motDePasse si nécessaire
        activity.save()
        return activity
    
    # Create your models here.
class Gyroscope(models.Model):
    x=models.FloatField()
    y=models.FloatField()
    z=models.FloatField()
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)
    @classmethod
    def create_Gyroscope(cls,x,y,z,activity ):
        gyroscope = cls(x=x,y=y,z=z, activity=activity)
        gyroscope.save()
        return gyroscope
    
     # Create your models here.
class Acceleration(models.Model):
    x=models.FloatField()
    y=models.FloatField()
    z=models.FloatField()
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)
    @classmethod
    def create_Acceleration(cls,x,y,z,activity ):
        acceleration = cls(x=x,y=y,z=z, activity=activity)
        acceleration.save()
        return acceleration

     # Create your models here.
class Gylocation(models.Model):
    speed=models.FloatField()
    heading=models.FloatField()
    altitude=models.FloatField()
    accuracy=models.FloatField()
    longitude=models.FloatField()
    altitudeAccuracy=models.FloatField()
    latitude=models.FloatField()


    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)
    @classmethod
    def create_Gylocation(cls,speed,heading,altitude,accuracy,longitude,altitudeAccuracy,latitude,activity ):
        gylocation = cls(speed=speed,heading=heading,altitude=altitude,accuracy=accuracy,longitude=longitude,altitudeAccuracy=altitudeAccuracy,latitude=latitude, activity=activity)
        gylocation.save()
        return gylocation