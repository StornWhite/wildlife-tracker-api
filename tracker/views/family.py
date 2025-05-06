from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView
)
from rest_framework import filters
from ..models import Family
from ..serializers.family import FamilySerializer


# Todo: add apidoc documentation


class FamilyRetrieveView(RetrieveAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class FamilyListCreateView(ListCreateAPIView):
    serializer_class = FamilySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Family.objects.all()
        herd_id = self.request.query_params.get('herd')
        if herd_id:
            queryset = queryset.filter(herd_id=herd_id)
        return queryset

