from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['POST', 'GET'])
def disruption(request):
    if request.method == 'POST':
        return add_disruption(request)
    elif request.method == 'GET':
        return get_disruption(request)


def add_disruption(request):
    return JsonResponse({"status": "Okay"}, status=200)


def get_disruption(request):
    return JsonResponse({"status": "Okay"}, status=200)
