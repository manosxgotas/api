from rest_framework.permissions import IsAuthenticated, BasePermission

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return (obj.usuario == request.user and
            request.method in ['GET', 'PUT', 'PATCH'])