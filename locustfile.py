from locust import HttpUser, task, between
import random


class PublicTransportUser(HttpUser):
    wait_time = between(1, 10)  # Simulate user wait times between requests

    @task(10)  # Higher weight means this runs more often
    def get_disruptions(self):
        self.client.get("/disruptions/")

    @task(1)
    def post_disruption(self):
        data = {
            "station_id": random.randint(1, 1000),
            "station_name": f"Station-{random.randint(1, 100)}",
            "disruption_bool": True,
            "disruption_text": "Failure",
            "timestamp": "2025-03-18T14:11:10+00:00"
        }
        self.client.post("/disruptions/", json=data)

    @task(2)
    def request_route(self):
        data = {
            "user": "user1",
            "latitude": 48.207806,
            "longitude": 16.372474,
            "bus": True,
            "tram": False,
            "subway": True
        }
        self.client.post("/routes/", json=data)

    @task(3)
    def get_station_arrival_times(self):
        num = random.randint(1, 100)
        data = {
            "station_id": num,
            "station_name": f"Station-{num}",
        }
        self.client.post("/stations/", json=data)
