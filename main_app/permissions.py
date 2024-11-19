from rest_framework.permissions import BasePermission
from .models import *

SAFE_METHODS = ['GET', 'OPTIONS', 'HEAD']


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print(request.user_id)

        lot_id = request.GET.get('id')
        if lot_id is None:
            return False
        return Participant.objects.filter(id=lot_id, user_id=request.user_id).exists()
