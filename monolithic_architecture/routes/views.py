import json
from routes import routing
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def route_request(request):
    try:
        data = json.loads(request.body)

        user = data.get('user')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        bus = data.get('bus')
        tram = data.get('tram')
        subway = data.get('subway')

        response_data = {
            'start': "Test",
            'end': "Test",
            'message': f"Following data received from {user}: Latitude: {latitude}, Longitude: {longitude}, Bus: {bus}, Tram: {tram}, Subway: {subway}",
        }

        # return render(request, 'routes.html', response_data)

        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
