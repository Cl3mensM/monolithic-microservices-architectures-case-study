from django.urls import path
from .views import disruption

urlpatterns = [
    path('disruptions/', disruption),
]
