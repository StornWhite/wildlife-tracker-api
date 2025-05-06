from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView
)
from rest_framework import filters
from ..models import Herd
from ..serializers.herd import HerdSerializer


# Todo: add apidoc documentation


class HerdRetrieveView(RetrieveAPIView):
    queryset = Herd.objects.all()
    serializer_class = HerdSerializer


class HerdListView(ListAPIView):
    queryset = Herd.objects.all()
    serializer_class = HerdSerializer
    filter_backends = [filters.OrderingFilter]


class HerdCreateView(CreateAPIView):
    queryset = Herd.objects.all()
    serializer_class = HerdSerializer
