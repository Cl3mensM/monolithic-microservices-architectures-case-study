from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['POST', 'GET'])
def stations(request):
    if request.method == 'POST':
        return arrival_times(request)
    elif request.method == 'GET':
        return JsonResponse({"status": "GET method not allowed for this endpoint."}, status=405)


@api_view(['POST'])
def arrival_times(request):
    try:
        station_id = request.data['station_id']
        station_name = request.data['station_name']

        # Handle arrival times for exact station, if needed
        # For now, just return some dummy data

        response = {
            "station_id": station_id,
            "station_name": station_name,
            "next_arrivals": [
                2, 4, 6, 8, 10
            ]
        }

        return JsonResponse(response, status=200)

    except KeyError:
        return JsonResponse({"status": "Bad Request, invalid request body."}, status=400)
