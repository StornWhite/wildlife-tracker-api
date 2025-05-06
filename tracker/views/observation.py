from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView
)
from rest_framework import filters
from ..models import Observation
from ..serializers.observation import ObservationSerializer


# Todo: add apidoc documentation


class ObservationRetrieveView(RetrieveAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class ObservationListView(ListAPIView):
    serializer_class = ObservationSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Observation.objects.all()
        family_id = self.request.query_params.get('family')
        if family_id:
            queryset = queryset.filter(family_id=family_id)
        return queryset


# Todo implement mapbox vector tile view


class ObservationCreateView(CreateAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

