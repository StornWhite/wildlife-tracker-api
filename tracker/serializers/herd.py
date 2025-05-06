from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from ..models import Herd


class HerdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herd
        fields = '__all__'

    def validate(self, attrs):
        instance = Herd(**attrs)
        try:
            instance.full_clean()  # calls model.clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)
        return attrs
