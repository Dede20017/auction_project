from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = AuctionUser
        fields = ['name', 'surname', 'email', 'data_joined']

class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class LotSerializer(ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'
        # fields = ['number', 'name', 'area', 'price']

class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        # read_only_fields = ['date']

class BidSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class CurrencyRatesSerializer(serializers.Serializer):
    base = serializers.CharField(max_length=3)
    date = serializers.DateField()
    rates = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=4))