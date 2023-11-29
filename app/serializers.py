from .models import Ticket, FollowUp
from rest_framework import serializers

class ticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class followupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = ["author", "content"]