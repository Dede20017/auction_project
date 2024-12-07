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
        # if not request.user.is_authenticated:
        if not (request.user and request.user.is_authenticated):
            return False

        lot_id = request.GET.get('lot_id')
        if lot_id is None:
            lot_id = request.data.get('lot_id')  # If passed in the body

        if not lot_id:
            return False
        # print(request.user.id)
        print(Participant.objects.filter(lot_id=lot_id, user_id=request.user.id))
        if Participant.objects.filter(lot_id=lot_id, user_id=request.user.id).exists():
            return True

