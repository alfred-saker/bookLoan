from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# Je verifie si l'utilisateur est un super-user 
class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser and request.user.is_authenticated
    
# Seul les admins des livres et les superuser peuvent mettre à jour un livre
class IsAdminOrSuperUserOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Autoriser les méthodes safe (lecture seule) pour tous les utilisateurs.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Autoriser la mise à jour si l'utilisateur est le propriétaire du livre ou un super-utilisateur.
        return obj.user == request.user or request.user.is_superuser
    
    
class IsBookOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifiez si l'utilisateur est l'auteur du livre ou un superutilisateur
        return obj.book.user == request.user or request.user.is_superuser 