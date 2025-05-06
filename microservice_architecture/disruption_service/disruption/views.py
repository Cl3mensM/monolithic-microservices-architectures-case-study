from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
# from disruption.models import Disruption

# Create your views here.

url = "http://db-abstraction-service.default.svc.cluster.local:80/api/disruptions/"


@api_view(['POST', 'GET'])
def disruption(request):
    if request.method == 'POST':
        return add_disruption(request)
    elif request.method == 'GET':
        return get_disruption(request)


def add_disruption(request):
    return_data = requests.post(url, json=request.data).json()
    return JsonResponse(return_data, status=200)


def get_disruption(request):
    return_data = requests.get(url).json()
    return JsonResponse(return_data, safe=False, status=200)
