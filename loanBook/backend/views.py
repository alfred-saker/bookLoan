from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate,logout
import os

from backend.models import Book, Borrow
from backend.serializer import BookSerializer, UserSerializer, EmpruntSerializer,LoginSerializer
from backend.permission import IsAdminOrReadOnly
# from backend.pagination import LargeResultsSetPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes =  [IsAdminOrReadOnly]
    
class LoginViewSet(APIView):
    
    permission_classes =  [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

        # Authentification de l'utilisateur
        user = authenticate(username=username, password=password)
        user_url = reverse('user-detail', kwargs={'pk': user.pk})
        if user:
            # Création ou récupération du jeton d'authentification pour l'utilisateur
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id':user.id,
                'url': request.build_absolute_uri(user_url),
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'is_staff':user.is_staff
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewSet(APIView):
    
    def post(self, request, format=None):
        logout(request)
        return Response({"success": "Successfully logged out"}, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    # pagination_class = LargeResultsSetPagination


class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = EmpruntSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []

class DownloadBook(APIView):
    def get_book(request, pk):
        book = get_object_or_404(Book, pk=pk)
        file_path = os.path.join(settings.MEDIA_ROOT, book.pdf_file.name)

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={book.pdf_file.name}'

        book.number_dowload += 1
        book.save()

        return response


# userdjango2024 - saker