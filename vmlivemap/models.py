from django.db import models

# Create your models here.
class Route(models.Model):
    route_name = models.CharField(max_length=4)
    direction = models.CharField(max_length=1,default='U')
    def __str__(self):
        return self.route_name

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop_name = models.CharField(max_length=63)
    def __str__(self):
        return self.stop_name
