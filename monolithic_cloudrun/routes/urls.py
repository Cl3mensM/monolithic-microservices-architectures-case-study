from django.urls import path
from .views import route_request

urlpatterns = [
    path('routes/', route_request),
]
