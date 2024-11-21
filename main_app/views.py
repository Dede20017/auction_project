import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.db.models import Max

from .models import *
from .serializers import *
from .permissions import *

class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        surname = request.data.get('surname')
        try:
            user = AuctionUser.objects.create_user(email=email, password=password, name=name, surname=surname)
            return Response(data={'message': 'Registration success'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={'message': 'account with same email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(data={'message': 'email or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response(data={'message': 'Authorization success'}, status=status.HTTP_200_OK)

class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(AuctionUser, id=request.user.id)
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data={'message': 'data changed'}, status=status.HTTP_200_OK)
        else:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.user.id
        if user_id is None:
            return Response(data={'message': 'you need to add id'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(AuctionUser, id=user_id)
        user.delete()
        return Response(data={'message': 'user deleted'}, status=status.HTTP_200_OK)

class AreaApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        area_id = request.GET.get('id')
        if area_id is None:
            areas = Area.objects.all()
            data = AreaSerializer(areas, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            area = get_object_or_404(Area, id=area_id)
            data = AreaSerializer(area, many=False).data
            return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        area = AreaSerializer(data=request.data)
        if area.is_valid():
            area.save()
            return Response(data={'message': 'area added'}, status=status.HTTP_200_OK)
        else:
            return Response(data=area.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        area_id = request.GET.get('id')
        if area_id is None:
            return Response(data={'message': 'you forget to add id'}, status=status.HTTP_400_BAD_REQUEST)

        area = get_object_or_404(Area, id=area_id)
        area_serializer = AreaSerializer(area, data=request.data, partial=True)
        if area_serializer.is_valid():
            area_serializer.save()
            return Response(data={'message': 'area patched'}, status=status.HTTP_200_OK)
        else:
            return Response(data=area_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        area_id = request.GET.get('id')
        if area_id is None:
            return Response(data={'message': 'you forget to add id'}, status=status.HTTP_400_BAD_REQUEST)

        area = get_object_or_404(Area, id=area_id)
        area.delete()
        return Response(data={'message': 'area deleted'}, status=status.HTTP_200_OK)

class LotApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        lot_id = request.GET.get('id')
        if lot_id is None:
            lots = Lot.objects.all()
            data = LotSerializer(lots, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            lot = get_object_or_404(Lot, id=lot_id)
            data = LotSerializer(lot, many=False).data
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        lot = LotSerializer(data=request.data)
        if lot.is_valid():
            lot.save()
            return Response(data={'message': 'area added'}, status=status.HTTP_200_OK)
        else:
            return Response(data=lot.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        lot_id = request.GET.get('id')
        if lot_id is None:
            return Response(data={'message': 'you forget to add id'}, status=status.HTTP_400_BAD_REQUEST)

        lot = get_object_or_404(Lot, id=lot_id)
        lot_serializer = AreaSerializer(lot, data=request.data, partial=True)
        if lot_serializer.is_valid():
            lot_serializer.save()
            return Response(data={'message': 'lot patched'}, status=status.HTTP_200_OK)
        else:
            return Response(data=lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        lot_id = request.GET.get('id')
        if lot_id is None:
            return Response(data={'message': 'you forget to add id'}, status=status.HTTP_400_BAD_REQUEST)

        lot = get_object_or_404(Area, id=lot_id)
        lot.delete()
        return Response(data={'message': 'lot deleted'}, status=status.HTTP_200_OK)

class ParticipantApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):     #delete before deploy
        part_id = request.GET.get('id')
        if part_id is None:
            parts = Participant.objects.all()
            data = ParticipantSerializer(parts, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            part = get_object_or_404(Participant, id=part_id)
            data = ParticipantSerializer(part, many=False).data
            return Response(data, status=status.HTTP_200_OK)


    def post(self, request): #при нажатии JOIN
        lot_id = request.GET.get('id')
        lot = Lot.objects.get(id=lot_id)
        if lot.status != 'open':
            return Response(data={'message': 'Lot is not open'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = request.user.id

            if lot_id is None:
                return Response(data={'message': 'Lot ID is missing'}, status=status.HTTP_400_BAD_REQUEST)

            max_number = Participant.objects.filter(lot_id=lot_id).aggregate(Max('number'))['number__max'] or 0
            next_number = max_number + 1

            data = {
                "number": next_number,
                "user_id": user_id,
                "lot_id": lot_id,
                # "date": request.data.get('date')
            }
            part_serializer = ParticipantSerializer(data=data)
            if part_serializer.is_valid():
                part_serializer.save()
                return Response(data={'message': 'participant added'}, status=status.HTTP_200_OK)
            else:
                return Response(data=part_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BidApiView(APIView):
    permission_classes = [IsParticipant]
    # permission_classes = [IsAuthenticated]

    def get(self,request): #data for show in BID page
        lot_id = request.GET.get('id')
        if Lot.objects.filter(id=lot_id).exists():
            lot = Lot.objects.get(id=lot_id)
            if lot.status != 'open':
                return Response(data={'message': 'Lot is not open'}, status=status.HTTP_200_OK)
            else:
                user_id = request.user.id
                participant = Participant.objects.get(lot_id=lot_id, user_id=user_id)
                part_number = participant.number
                price = lot.price
                step_value = lot.step_value

                if Bid.objects.filter(lot_id=lot_id).exists():
                    max_step_number = Bid.objects.filter(lot_id=lot_id).aggregate(Max('step_number'))['step_number__max']
                    step_number = max_step_number + 1
                    total_price = price + step_number * step_value
                else:
                    step_number = 1
                    total_price = price + step_value

                data = {
                    "lot_id": lot_id,
                    "part_number": part_number,
                    "step_number": step_number,
                    "total_price": total_price
                }
                bid_serializer = BidSerializer(data=data)
                if bid_serializer.is_valid():
                    bid_serializer.save()
                    return Response(data=data, status=status.HTTP_200_OK)
                    # заменить сообщение на data
                else:
                    return Response(data=bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data={'message': 'Lot with this lot_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class LotSearchApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get('search')
        if Lot.objects.filter(name__contains=search).exists():
            lot_by_name = Lot.objects.filter(name__contains=search)

            lots = set()
            lots = lots.union(lot_by_name)
            # paginator = PageNumberPagination()
            # paginator.page_size = 2
            # paginated_lots = paginator.paginate_queryset(lots, request)

            data = LotSerializer(lots, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'lot not found'}, status=status.HTTP_400_BAD_REQUEST)

class LotOrderApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.GET.get('date')
        lots = Lot.objects.all()

        if date is not None:
            if date == 'desc':
                lots = lots.order_by('-date')
            elif date == 'asc':
                lots = lots.order_by('date')
        # paginator = PageNumberPagination()
        # paginator.page_size = 2
        # paginated_lots = paginator.paginate_queryset(lots, request)
        data = LotSerializer(lots, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)