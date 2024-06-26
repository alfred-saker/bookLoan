from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Book,CustomUser,BookVersion
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
import os
import uuid


User = get_user_model()

class BookVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models=BookVersion
        fields = '__all__'
        exclude = ['created_at']
        
    def Validate_data(self, data):
        if not data.get("book"):
            raise serializers.ValidateError("Book:Book is required")
        if not data.get("book_type"):
            raise serializers.ValidationError("Book Type: Book type is required")
        if not data.get("language"):
            raise serializers.ValidationError("Language : Language is required")
        if not data.get("number_pages"):
            raise serializers.ValidationError("Number page : Number page is required")
        if not data.get("time_read_book"):
            raise serializers.ValidationError("Time read book : time read book is required")
        return data
        
        

class BookSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        lookup_field='id' 
    )
    class Meta:
        model = Book
        fields = ['url', 'author', 'summary','title', 'year_publication','download_count','category','user','slug','rating_sum','rating_count','id']
        read_only_fields = ["id","slug","rating_sum","download_count"]
        
    def validate(self, data):
        if not data.get("author"):
            raise serializers.ValidationError({"author": "Enter the author name"})
        if not data.get("title"):
            raise serializers.ValidationError({"title": "Enter the title of book"})
        if not data.get("summary"):
            raise serializers.ValidationError({"summary": "Enter the summary text"})
        if not data.get("year_publication"):
            raise serializers.ValidationError({"year_publication": "Enter the year publication"})
        if not data.get("category"):
            raise serializers.ValidationError({"category": "Enter the category name"})
        return data  # Always return the cleaned data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title',instance.title) 
        instance.summary = validated_data.get('summary',instance.summary) 
        instance.year_publication = validated_data.get('year_publication',instance.year_publication) 
        instance.category = validated_data.get('category',instance.category) 
        instance.save()
        return instance
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'first_name','last_name', 'email', 'user_type', 'biography', 'phone_number', 'country', 'total_book_download', 'image', 'created_at','password']
        read_only_fields = ['total_book_download', 'created_at']

        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'user-detail', 'lookup_field': 'pk'}
        }
    # Je crée une fois le user de base avec un role de niveau 2 par defaut.
    def create(self, validated_data):
        username = validated_data.get('username')  # Utiliser get pour éviter KeyError (erreur de clé)
        email = validated_data.get('email')  # Utiliser get pour éviter KeyError
        password = validated_data.get('password')  # Utiliser get pour éviter KeyError
        
        if not username:
            raise serializers.ValidationError({"Username": "Username is required."})
        if not email:
            raise serializers.ValidationError({"Email": "Email is required."})
        if not password:
            raise serializers.ValidationError({"Password": "Password is required."})
        
        # Je verifie le password avant de le save dans la BD
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            biography=validated_data.get('biography', ''),
            phone_number=validated_data.get('phone_number', ''),
            country=validated_data.get('country', ''),
            user_type=validated_data.get('user_type', 2)  # Default to 'Lecteur'
        )
        user.set_password(password)
        user.save()

        if 'image' in validated_data:
            user.image = validated_data['image']
            user.save()
        return user  
    
    # Mise à jour du profil user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)  # Utiliser la valeur actuelle comme défaut
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)

        instance.save()
        return instance

    
class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')  # Utiliser get pour éviter KeyError
        new_password = data.get('new_password')  # Utiliser get pour éviter KeyError
        confirm_password = data.get('confirm_password')  # Utiliser get pour éviter KeyError
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        # Vérifiez que l'ancien mot de passe est correct
        if not self.instance.check_password(old_password):
            raise ValidationError({"old_password": "L'ancien mot de passe n'est pas correct."})

        # Vérifiez que les nouveaux mots de passe correspondent
        if new_password != confirm_password:
            raise ValidationError({"confirm_password": "Les nouveaux mots de passe ne correspondent pas."})

        # Vous pouvez ajouter des vérifications supplémentaires ici si nécessaire
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
class ImageUserUpdateSerializer(serializers.Serializer):
    
    image = serializers.ImageField(required=True)

    def validate_image(self, value):
        MAX_SIZE = 12000000  # 12 MB

        # `value` est l'objet fichier ici, pas un dictionnaire
        if value.size > MAX_SIZE:
            raise ValidationError("Image volumineuse, taille maximale autorisée est de 12 MB.")

        # Vérification du format de l'image
        valid_extensions = ['jpg', 'jpeg', 'png', 'svg']
        extension = os.path.splitext(value.name)[1][1:].lower()
        print(extension)
        if extension not in valid_extensions:
            raise ValidationError("Veuillez uploader une image du type png, jpeg, jpg, svg.")
        print(value)
        return value

    def update(self, instance, validated_data):
        image = validated_data.get('image', None)
        if image:
            # Générer un nouveau nom de fichier sécurisé
            new_filename = f"{uuid.uuid4()}{os.path.splitext(image.name)[1].lower()}"
            # Lire le contenu du fichier
            image_content = ContentFile(image.read())
            # Sauvegarder le nouveau fichier image
            instance.image.save(new_filename, image_content, save=False)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    
    
    
    
    







