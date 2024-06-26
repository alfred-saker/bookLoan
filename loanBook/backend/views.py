from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404,FileResponse
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

from backend.models import Book, CustomUser
from backend.serializer import BookSerializer, ImageUserUpdateSerializer, CustomUserSerializer,PasswordSerializer,LoginSerializer
from backend.permission import IsAdminOrReadOnly, IsSuperUser


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):

        if self.action in ['create','update','partial_update']:
            return [IsAdminOrReadOnly(),IsSuperUser(), permissions.IsAuthenticated()]
        elif self.action in ["retrieve","list"]:
            return [permissions.AllowAny()]
        else:
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
    


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    
    def get_permissions(self):
        """
        Instantier et retourner la liste des permissions que cette vue requiert.
        """
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





# class BorrowViewSet(viewsets.ModelViewSet):
#     queryset = Borrow.objects.all()
#     serializer_class = EmpruntSerializer
#     authentication_classes = [TokenAuthentication]
#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             user = self.request.user
#             # Filtrer les emprunts en fonction de l'utilisateur actuellement authentifié
#             return Borrow.objects.filter(user=user)
#         else:
#             # Si l'utilisateur n'est pas authentifié, renvoyer un queryset vide
#             return Borrow.objects.none()

class DownloadBook(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk):
        # Récupérer le livre par son ID
        book = get_object_or_404(Book, pk=pk)

        # Chemin du fichier PDF
        file_path = os.path.join(settings.MEDIA_ROOT, book.pdf_file.name)

        # Debug: Afficher le chemin du fichier
        print(f"Chemin du fichier: {file_path}")

        # Vérifier que le fichier existe
        if not os.path.exists(file_path):
            raise Http404("Le fichier n'existe pas")

        # Vérifier les permissions
        if not os.access(file_path, os.R_OK):
            raise Http404("Permissions de fichier insuffisantes")

        # Créer la réponse HTTP pour le téléchargement du fichier
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'

        # Incrémenter le compteur de téléchargements
        book.download_count += 1
        book.save()

        return response


# class UserChangePasswordView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminOrReadOnly]
#     def patch(self, request, pk):
#         User = get_user_model()
        
#         user = User.objects.get(pk=pk)
#         serializer = ChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             old_password = serializer.validated_data.get('old_password')
#             new_password = serializer.validated_data.get('new_password')
#             # Vérifier l'ancien mot de passe
#             if not user.check_password(old_password):
#                 return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

#             # Mettre à jour le mot de passe de l'utilisateur
#             user.set_password(new_password)
#             user.save()

#             return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# userdjango2024 - saker