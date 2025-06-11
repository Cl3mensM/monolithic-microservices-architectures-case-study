from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from disruptions.models import Disruption


@api_view(['POST', 'GET'])
def disruption(request):
    if request.method == 'POST':
        return add_disruption(request)
    elif request.method == 'GET':
        return get_disruption(request)


def add_disruption(request):
    try:
        station_id = request.data['station_id']
        station_name = request.data['station_name']
        disruption_bool = request.data['disruption_bool']
        disruption_text = request.data['disruption_text']
        timestamp = request.data['timestamp']

        # True if disruption is happening, False if disruption is resolved
        if disruption_bool:
            disruption = Disruption(station_id=station_id, station_name=station_name,
                                    disruption_text=disruption_text, disruption_start=timestamp)
            disruption.save()
        else:
            Disruption.objects.filter(station_id=station_id).delete()

    except KeyError:
        return JsonResponse({"status": "Bad Request, invalid request body."}, status=400)

    return JsonResponse({"status": "Okay"}, status=200)


def get_disruption(request):
    disruptions = Disruption.objects.all()

    if disruptions.count() == 0:
        return JsonResponse({"status": "Currently no disruptions!"}, status=200)

    response = []
    for disruption in disruptions:
        response.append({
            "station_id": disruption.station_id,
            "station_name": disruption.station_name,
            "disruption_text": disruption.disruption_text,
            "timestamp": disruption.disruption_start
        })

    return JsonResponse(response, safe=False, status=200)
