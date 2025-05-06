from rest_framework import serializers
from ..models import Herd


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herd
        fields = '__all__'
