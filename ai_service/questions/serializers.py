from rest_framework import serializers
from .models import AIRequest

class AIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRequest
        fields = "__all__"
