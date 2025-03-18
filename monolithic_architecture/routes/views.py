import json
from routes import routing
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def route_request(request):
    try:
        data = json.loads(request.body)

        required_fields = ['user', 'latitude',
                           'longitude', 'bus', 'tram', 'subway']
        missing_fields = [
            field for field in required_fields if field not in data]

        if missing_fields:
            return JsonResponse(
                {"status": f"Missing required fields: {', '.join(missing_fields)}"},
                status=400
            )

        user = data.get('user')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        bus = data.get('bus')
        tram = data.get('tram')
        subway = data.get('subway')

        if bus is False and tram is False and subway is False:
            return JsonResponse({"status": "Please select at least one mode of transportation"}, status=400)

        # response_data = {
        #     'start': "Test",
        #     'end': "Test",
        #     'message': f"Following data received from {user}: Latitude: {latitude}, Longitude: {longitude}, Bus: {bus}, Tram: {tram}, Subway: {subway}",
        # }

        # return render(request, 'routes.html', response_data)

        route, stop = routing.route_for_user_request(
            latitude, longitude, bus, tram, subway)
        response_data = {
            "station": stop["name"],
            "route": route
        }

        return JsonResponse(response_data, safe=False, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "Bad Request, invalid request body."}, status=400)
