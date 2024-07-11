
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Book,CustomUser,BookVersion,FavoriteBookUser,Rating, Comment
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
import os
import uuid


User = get_user_model()

class CommentBookSerializer(serializers.HyperlinkedModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.HyperlinkedRelatedField(
        view_name = "user-detail",
        read_only = True,
        lookup_field = 'pk'
    )
    book = serializers.HyperlinkedRelatedField(
        view_name="book-detail",
        queryset=Book.objects.all(),
        lookup_field='pk'
    )
    class Meta:
        model = Comment
        fields = ['url','user','book','content','replies']
    
    # Je verifie si la reponse du commentaire existe deja, si oui je met juste a jour la reponse du commentaire. car la reponse d'un commentaire est limité à 1 niveau de profondeur.
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentBookSerializer(obj.replies.all(), many=True, context=self.context).data
        return None

class RatingBookSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        read_only = True,
        lookup_field = 'pk'
    )
    book = serializers.HyperlinkedRelatedField(
        view_name="book-detail",
        queryset = Book.objects.all(),
        lookup_field = "pk"
    )
    class Meta:
        model = Rating
        fields = ['url','user','book','score']
    
    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("The score must be between 1 and 5.")
        return value
    def create(self, validated_data):
        # Je fais un fecth dans la bd pour verifié si existe deja une note pour ce livre , si oui je l'update et si non je le crée
        user = self.context['request'].user
        book = validated_data['book']
        score = validated_data['score']

        # Assurez-vous que l'utilisateur connecté est utilisé
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to rate a book.")

        # Mettez à jour ou créez la note
        rating, created = Rating.objects.update_or_create(
            user=user,
            book=book,
            defaults={'score': score}
        )
        return rating

class FavoriteBookSerializer(serializers.HyperlinkedModelSerializer):
    
    user = serializers.HyperlinkedRelatedField(
        view_name = "user-detail",
        read_only = True,
        lookup_field = "pk"
    )
    book = serializers.HyperlinkedRelatedField(
        view_name="book-detail",
        queryset=Book.objects.all(),
        lookup_field='pk' ,
        required = False
    )
    book_version = serializers.HyperlinkedRelatedField(
        view_name="bookversion-detail",
        queryset=BookVersion.objects.all(),
        lookup_field = 'pk',
        required = False
    )
    class Meta:
        model = FavoriteBookUser
        fields = ['url','user', 'book', 'book_version', 'is_favorite']
        
    
    def validate(self, data):
        book = data.get("book")
        book_version = data.get("book_version")

        if not book and not book_version:
            raise serializers.ValidationError("Either 'book' or 'book_version' must be provided.")
        
        if book and book_version:
            raise serializers.ValidationError("You can only favorite either a book or a book version, not both.")

        user = self.context['request'].user

        # Check if the favorite already exists
        if book and FavoriteBookUser.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("This book is already in your favorites.")
        
        if book_version and FavoriteBookUser.objects.filter(user=user, book_version=book_version).exists():
            raise serializers.ValidationError("This book version is already in your favorites.")

        return data

    def create(self, validated_data):
        return FavoriteBookUser.objects.create(**validated_data)
    
    # def update(self,instance,validated_data):

    #     is_favorite = validated_data.get("is_favorite",instance.is_favorite)
    #     instance.is_favorite = is_favorite
    #     instance.save()
    #     return instance
        
class BookVersionSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.HyperlinkedRelatedField(
        view_name='book-detail',
        queryset=Book.objects.all(),
        lookup_field='pk' 
    )

    class Meta:
        model = BookVersion
        exclude = ['created_at', 'updated_at']
        
    def validate(self, data):
        # Validation générale pour les champs requis
        if not data.get("book"):
            raise serializers.ValidationError({"book": "Book is required"})
        if not data.get("book_type"):
            raise serializers.ValidationError({"book_type": "Book type is required"})
        if not data.get("language"):
            raise serializers.ValidationError({"language": "Language is required"})
        if not data.get("picture_file"):
            raise serializers.ValidationError({"picture_file": "Picture file is required"})
        if not data.get("file"):
            raise serializers.ValidationError({"file": "File is required"})

        # Validation du fichier image
        self.validate_picture_file(data.get("picture_file"))

        # Validation du fichier du livre en fonction du type
        book_type = data.get('book_type')
        file_book = data.get('file')

        if book_type == 'pdf':
            self.validate_pdf_file(file_book)
        elif book_type == 'ebook':
            self.validate_epub_file(file_book)
        elif book_type == 'audio':
            self.validate_audio_file(file_book)
        else:
            raise serializers.ValidationError("Veuillez entrer un format de livre correct. Formats autorisés: pdf, ebook, audio")

        return data

    def validate_picture_file(self, value):
        # Validation de l'image de couverture avec consolidation des vérifications
        MAX_SIZE = 12000000  # 12 MB
        valid_extensions = ['jpg', 'jpeg', 'png', 'svg']
        
        # Print statements for debugging
        print(f"File name: {value.name}")
        print(f"File size: {value.size}")

        extension = os.path.splitext(value.name)[1][1:].lower()
        print(f"File extension: {extension}")

        if value.size > MAX_SIZE:
            raise serializers.ValidationError("Image volumineuse, taille maximale autorisée est de 12 MB.")
        if extension not in valid_extensions:
            raise serializers.ValidationError("Veuillez uploader une image du type png, jpeg, jpg, svg.")
        print("true picture file")
        return value

    def validate_pdf_file(self, value):
        # Validation spécifique pour les fichiers PDF
        MAX_SIZE = 50000000  # 50 MB
        if value.size > MAX_SIZE:
            raise serializers.ValidationError(f"Le fichier PDF est trop volumineux, taille maximale autorisée est de {MAX_SIZE / 1000000} MB.")

        extension = os.path.splitext(value.name)[1][1:].lower()
        if extension != 'pdf':
            raise serializers.ValidationError("Le fichier doit être au format PDF.")
        print("true file book")
        return value

    def validate_epub_file(self, value):
        # Validation spécifique pour les fichiers EPUB
        MAX_SIZE = 50000000  # 50 MB
        if value.size > MAX_SIZE:
            raise serializers.ValidationError(f"Le fichier EPUB est trop volumineux, taille maximale autorisée est de {MAX_SIZE / 1000000} MB.")

        extension = os.path.splitext(value.name)[1][1:].lower()
        if extension != 'epub':
            raise serializers.ValidationError("Le fichier doit être au format EPUB.")
        print("true file EPUB")
        return value

    def validate_audio_file(self, value):
        # Validation spécifique pour les fichiers audio
        MAX_SIZE = 50000000  # 50 MB
        VALID_AUDIO_EXTENSIONS = ['mp3', 'm4b', 'aac', 'wav', 'ogg']
        if value.size > MAX_SIZE:
            raise serializers.ValidationError(f"Le fichier audio est trop volumineux, taille maximale autorisée est de {MAX_SIZE / 1000000} MB.")

        extension = os.path.splitext(value.name)[1][1:].lower()
        if extension not in VALID_AUDIO_EXTENSIONS:
            allowed_formats = ", ".join(f"'{ext}'" for ext in VALID_AUDIO_EXTENSIONS)
            raise serializers.ValidationError(f"Format de fichier non autorisé! Formats autorisés pour les livres audio: {allowed_formats}.")
        print("True audio file")
        return value


    def create(self, validated_data):
        # Création d'une instance de BookVersion
        return BookVersion.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
    # Récupérer les nouvelles valeurs ou conserver les anciennes
        book = validated_data.get('book', instance.book)
        book_type = validated_data.get('book_type', instance.book_type)
        language = validated_data.get('language', instance.language)

        # Mettre à jour les champs de l'instance
        instance.book = book
        instance.book_type = book_type
        instance.language = language
        instance.picture_file = validated_data.get('picture_file', instance.picture_file)
        instance.number_pages = validated_data.get('number_pages', instance.number_pages)
        instance.time_read_book = validated_data.get('time_read_book', instance.time_read_book)
        instance.file = validated_data.get('file', instance.file)

        # Sauvegarder les modifications de l'instance
        instance.save()
        
        # Retourner l'instance mise à jour
        return instance   

class BookSerializer(serializers.HyperlinkedModelSerializer):
    
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        lookup_field='pk' 
    )
    comments = CommentBookSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['url', 'author', 'summary','title', 'year_publication','download_count','category','user','slug','rating_sum','rating_count','id','comments']
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
        fields = ['url', 'username', 'first_name','last_name', 'email', 'user_type', 'biography', 'phone_number', 'country', 'total_book_download', 'image', 'created_at','password','is_staff']
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
        # Si le user_type est 1 alors le user est un admin(Editeur) dans le cas contraire il est juste un simple user (lecteur)
        if user.user_type == 1:
            user.is_staff = True
        else:
            user.is_staff = False
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
    
    
    
    
    
    







