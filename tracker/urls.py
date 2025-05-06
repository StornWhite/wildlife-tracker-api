"""
URL configuration for tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views.herd import (
    HerdRetrieveView,
    HerdListCreateView,
)
from .views.family import (
    FamilyRetrieveView,
    FamilyListCreateView,
)
from .views.observation import (
    ObservationRetrieveView,
    ObservationListCreateView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'herds/<str:pk>/',
        HerdRetrieveView.as_view(),
        name='herd-detail'
    ),

    path(
        'herds/',
        HerdListCreateView.as_view(),
        name='herd-list'
    ),

    path(
        'families/<str:pk>/',
        FamilyRetrieveView.as_view(),
        name='family-detail'
    ),

    path(
        'families/',
        FamilyListCreateView.as_view(),
        name='family-list'
    ),

    path(
        'observations/<str:pk>/',
        ObservationRetrieveView.as_view(),
        name='observation-detail'
    ),

    path(
        'observations/',
        ObservationListCreateView.as_view(),
        name='observation-list'
    ),
]
