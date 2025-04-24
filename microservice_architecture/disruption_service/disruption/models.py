from django.db import models

# Create your models here.


class Disruption(models.Model):
    station_id = models.IntegerField()
    station_name = models.CharField(max_length=100)
    disruption_text = models.TextField()
    disruption_start = models.DateTimeField()

    class Meta:
        db_table = "disruption_disruption"
