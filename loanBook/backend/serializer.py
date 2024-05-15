from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import Borrow, Book
from django.contrib.auth.models import Group, User

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['url', 'author', 'description','title', 'year_publication','type_book','number_dowload','gender','user','status_book','pdf_file','picture_books']
        

class EmpruntSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'books']
        

class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    class Meta:
        model = User
        fields = ('url','username', 'password', 'email', 'first_name', 'last_name','is_staff')
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)