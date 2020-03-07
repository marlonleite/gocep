"""
    gocep URL Configuration
"""
from django.urls import path, include
from rest_framework import routers

from client import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api/<int:zip_code>/', views.AddressApiView.as_view(), name='gocep-zip_code'),
    path('api/', views.AddressApiView.as_view(), name='gocep-address')
]
