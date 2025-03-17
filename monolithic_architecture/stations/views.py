from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['POST'])
def stations(request):
    return JsonResponse({"status": "Okay"}, status=200)
