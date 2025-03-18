from django.test import TestCase
from routes import routing
from disruptions.models import Disruption


class RoutingTestCase(TestCase):
    def test_route_for_user_request(self):
        # Arrange
        latitude = 48.207806
        longitude = 16.372474
        bus = True
        tram = False
        subway = True

        # Act
        route, stop = routing.route_for_user_request(
            latitude, longitude, bus, tram, subway)

        # Assert
        self.assertIsNotNone(route, "Route should not be None")
        self.assertIsNotNone(stop, "Stop should not be None")
        self.assertIsInstance(
            stop["name"], str, "Stop name should be a string")
        self.assertEqual(stop["name"], "Stephansplatz",
                         "Stop name should be Stephansplatz")
        self.assertEqual(route, [286405440, 3175113342, 3175113349, 301888805, 4180630294, 4181009993, 4181066389],
                         "Route should be correct")

    def test_route_for_user_request_with_disruption(self):
        # Arrange
        latitude = 48.208084
        longitude = 16.379504
        bus = True
        tram = False
        subway = True
        disruption = Disruption(
            station_id=286405440, station_name="Stubentor", disruption_text="Test", disruption_start="2021-06-01T12:00:00Z")
        disruption.save()

        # Act
        route, stop = routing.route_for_user_request(
            latitude, longitude, bus, tram, subway)

        # Assert
        self.assertIsNotNone(route, "Route should not be None")
        self.assertIsNotNone(stop, "Stop should not be None")
        self.assertIsInstance(
            stop["name"], str, "Stop name should be a string")
        self.assertEqual(stop["name"], "Riemergasse",
                         "Stop name should be Riemergasse")
        self.assertEqual(route, [60060217, 12221937460, 4841566555, 2886812626, 2016564311, 1462300920, 60143984, 291221759],
                         "Route should be correct")
        disruption.delete()
