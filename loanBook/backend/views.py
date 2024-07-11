from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404,FileResponse,JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from rest_framework import permissions, viewsets,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout,get_user_model
import os

from backend.models import Book, CustomUser, BookVersion, FavoriteBookUser, Rating, Comment
from backend.serializer import BookSerializer,BookVersionSerializer, ImageUserUpdateSerializer, CustomUserSerializer,PasswordSerializer,LoginSerializer,FavoriteBookSerializer, RatingBookSerializer, CommentBookSerializer
from backend.permission import IsAdminOrReadOnly, IsSuperUser, IsAdminOrSuperUserOrOwner,IsBookOwnerOrSuperUser


class CommentBookViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentBookSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_superuser:
            return Response({"detail": "You do not have permission to delete this rating."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        book = instance.book
        book.rating_sum -= instance.score
        book.rating_count -= 1
        book.save()
        instance.delete()

class RatingBookViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to update this rating."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_superuser:
            return Response({"detail": "You do not have permission to delete this rating."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        book = instance.book
        book.rating_sum -= instance.score
        book.rating_count -= 1
        book.save()
        instance.delete()

class FavoriteBookUserViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBookUser.objects.all()
    serializer_class = FavoriteBookSerializer
    permissions_class = [permissions.IsAuthenticated]
    
    # J'ajoute un livre en favorie à partir de l'user connecté.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_superuser:
            return Response({"detail": "You do not have permission to delete this favorite."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):

        if self.action in ['create']:
            # Pour créer, on pourrait envisager que seuls les utilisateurs authentifiés ou les superutilisateurs puissent créer des livres
            return [permissions.IsAuthenticated(), IsSuperUser(), IsAdminOrReadOnly()]
        elif self.action in ['update', 'partial_update']:
            # Pour mettre à jour, on exige que l'utilisateur soit le propriétaire du livre ou un super-utilisateur
            return [IsAdminOrSuperUserOrOwner()]
        elif self.action in ['retrieve', 'list']:
            # Pour lire ou lister, tous les utilisateurs peuvent accéder
            return [permissions.AllowAny()]
        else:
            # Pour toutes les autres actions, l'accès est donné aux utilisateurs authentifiés
            return [permissions.IsAuthenticated()]
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser or not request.user.is_staff:  
            return Response({"detail": "You do not have permission to delete this book."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        print('delete')
    
class BookVersionViewSet(viewsets.ModelViewSet):
    queryset = BookVersion.objects.all()
    serializer_class = BookVersionSerializer
    
    def get_permissions(self):

        if self.action in ['create']:
            # Pour créer, on pourrait envisager que seuls les utilisateurs authentifiés ou les superutilisateurs puissent créer des versions de livres
            return [permissions.IsAuthenticated(), IsSuperUser(), IsAdminOrReadOnly()]
        elif self.action in ['update', 'partial_update']:
            # Pour mettre à jour, on exige que l'utilisateur soit le propriétaire du livre ou un super-utilisateur
            return [IsBookOwnerOrSuperUser()]
        elif self.action in ['retrieve', 'list']:
            # Pour lire ou lister, tous les utilisateurs peuvent accéder
            return [permissions.AllowAny()]
        else:
            # Pour toutes les autres actions, l'accès est donné aux utilisateurs authentifiés
            return [permissions.IsAuthenticated()]
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.book.user !=request.user and not request.user.is_superuser:  
            return Response({"detail": "You do not have permission to delete this book versions."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        print('delete')

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'
    
    def get_permissions(self):

        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ["retrieve","list"]:
            return [IsSuperUser()]
        elif self.action in ['update', 'partial_update', 'update_password','update_image_user']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['patch'], url_path='update_password')
    def update_password(self, request, pk=None):

        user = self.get_object()
        password = request.data.get('new_password')
        if request.user != user and not request.user.is_superuser:
            return Response({"error": "Vous n'êtes pas autorisé à modifier ce mot de passe."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PasswordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if user.check_password(password):
                print("mot de passe changé")
                return Response({"status": "password updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "password not updated correctly"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['patch'], url_path='update_image_user')
    def UpdateImageUser(self, request, pk=None):
        user = self.get_object()
        if request.user != user and not request.is_superuser:
            return Response({"error": "Vous n'êtes pas autorisé à mettre à jour cette image."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ImageUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "Image updated successfully",
                "image_url": user.image.url
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser:  
            return Response({"detail": "You do not have permission to delete this user."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        print('delete')

        
class LoginViewSet(APIView):
    
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        user_url = reverse('user-detail', kwargs={'pk': user.pk})
        user_url = request.build_absolute_uri(user_url)
        print(user_url)

        response_data = {
            'token': token.key,
            'id': user.id,
            'url': user_url,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class LogoutViewSet(APIView):
    
    def post(self, request, format=None):
        logout(request)
        return Response({"success": "Successfully logged out"}, status=status.HTTP_200_OK)


class DownloadBook(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, file_type):
        # Récupérer le livre par son ID
        book = get_object_or_404(Book, pk=pk)

        # Déterminer le chemin du fichier en fonction du type de fichier demandé
        if file_type == 'pdf':
            file_path = os.path.join(settings.MEDIA_ROOT, book.pdf_file.name)
            content_type = 'application/pdf'
        elif file_type == 'audio':
            file_path = os.path.join(settings.MEDIA_ROOT, book.audio_file.name)
            content_type = 'audio/mpeg'
        elif file_type == 'ebook':
            file_path = os.path.join(settings.MEDIA_ROOT, book.ebook_file.name)
            content_type = 'application/epub+zip'
        else:
            raise Http404("Type de fichier non supporté")

        # Vérifier que le fichier existe
        if not os.path.exists(file_path):
            raise Http404("Le fichier n'existe pas")

        # Vérifier les permissions
        if not os.access(file_path, os.R_OK):
            raise Http404("Permissions de fichier insuffisantes")

        # Créer la réponse HTTP pour le téléchargement du fichier
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'

        # Incrémenter le compteur de téléchargements
        book.download_count += 1
        book.save()

        return response

def custom_404_view(request, exception=None):
    response_data = {
        "error": "Page not found",
        "status_code": 404
    }
    return JsonResponse(response_data, status=404)
