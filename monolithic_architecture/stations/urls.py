from django.urls import path
from .views import stations

urlpatterns = [
    path('stations/', stations),
]
