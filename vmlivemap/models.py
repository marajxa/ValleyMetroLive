from django.db import models

# Create your models here.
class Route(models.Model):
    route_name = models.CharField(max_length=4)
    direction = models.CharField(max_length=16,default='U')
    def __str__(self):
        return f"{self.route_name} {self.direction}"

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop_number = models.IntegerField()
    stop_name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return f"{self.stop_number} {self.stop_name}"
