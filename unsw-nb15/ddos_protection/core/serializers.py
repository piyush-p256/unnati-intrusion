from rest_framework import serializers
from .models import TrafficLog

class TrafficLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLog
        fields = ['id', 'ip_address', 'timestamp', 'attack_type', 'blocked']
