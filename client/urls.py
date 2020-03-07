from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddressApiView.as_view(), name='gocep-address'),
    path('<int:zip_code>/', views.AddressApiView.as_view(), name='gocep-zip_code'),
]
