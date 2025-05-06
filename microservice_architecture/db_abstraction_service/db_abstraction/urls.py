from django.urls import path
from . import views

urlpatterns = [
    path('disruptions/', views.disruption),
]
