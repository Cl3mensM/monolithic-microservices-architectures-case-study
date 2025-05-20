from locust import HttpUser, task, between, constant
import random
import json


class PublicTransportUser(HttpUser):
    # wait_time = between(1, 10)
    wait_time = constant(5)  # Wait for 5 second between tasks

    @task(5)
    def get_disruptions(self):
        self.client.get("/disruptions/")

    @task(2)
    def request_route(self):
        # Near Stubentor
        # "latitude": 48.208084,
        # "longitude": 16.379504,
        # Near Stephansplatz
        # "latitude": 48.207806,
        # "longitude": 16.372474,
        data = {
            "user": "user1",
            "latitude": 48.208084,
            "longitude": 16.379504,
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


class AdminUser(HttpUser):
    """Simulate an admin user who can add disruptions."""
    wait_time = constant(60)  # Wait for 60 seconds between tasks
    disruptions_sent = 0
    fixed_count = 1

    # Preload the disruptions from stations.json
    with open("stations.json", "r") as f:
        disruptions_data = json.load(f)

    @task(1)
    def post_disruption(self):
        if self.disruptions_sent < len(self.disruptions_data):
            data = self.disruptions_data[self.disruptions_sent]
            self.client.post("/disruptions/", json=data)
            self.disruptions_sent += 1
        else:
            self.environment.runner.quit()  # Optional: stop this user after 2 requests
