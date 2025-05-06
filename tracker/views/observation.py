from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView
)
from rest_framework import filters
from ..models import Observation
from ..serializers.observation import ObservationSerializer


# Todo: add apidoc documentation


class ObservationRetrieveView(RetrieveAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class ObservationListCreateView(ListCreateAPIView):
    serializer_class = ObservationSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        # todo: implement query by location
        queryset = Observation.objects.all()
        family_id = self.request.query_params.get('family')
        if family_id:
            queryset = queryset.filter(family_id=family_id)
        return queryset


# Todo implement mapbox vector tile view
