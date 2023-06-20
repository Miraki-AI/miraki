from .models import Organization
from rest_framework import serializers

class OrganizationSerializer(serializers.Serializer):
    class Meta:
        model = Organization
        fields = ('name', 'paid_until', 'on_trial', 'created_on')