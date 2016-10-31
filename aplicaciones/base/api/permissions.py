from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.usuario == request.user and
                request.method in ['GET', 'PUT', 'PATCH'])


class IsOwnerDonacion(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.registro.donante.usuario == request.user and
                request.method in ['GET', 'PUT', 'PATCH', 'DELETE'])


class IsOwnerSolicitud(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.donante.usuario == request.user and
                request.method in ['GET', 'PUT', 'PATCH', 'DELETE'])
