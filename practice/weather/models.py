from django.db import models
from django.utils import timezone
import datetime

class City(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    coord_lon = models.FloatField()
    coord_lat = models.FloatField()

    def __str__(self):
        return str(self.city)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Cloud(models.Model):
    id = models.AutoField(primary_key=True)
    cloud = models.CharField(max_length=100)
    cloud_id = models.CharField(max_length=3)
    icon = models.ImageField(null=True, upload_to="cloudness_icon")

    def __str__(self):
        return str(self.cloud)

    class Meta:
        verbose_name = "Cloud"
        verbose_name_plural = "Clouds"

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City)
    date = models.DateField()
    description = models.CharField(max_length=100) #описание погоды, заголовок
    cloudiness = models.ForeignKey(Cloud) #облачность, описание
    temp_max = models.IntegerField() #максимальная температура
    temp_min = models.IntegerField() #минимальная температура
    wind_speed = models.FloatField() #скорость ветра, м/с
    wind_description = models.CharField(max_length=100) #скорость ветра, описание
    wind_degree = models.IntegerField() #направление ветра, градусы
    wind_direction = models.CharField(max_length=100) #направление ветра, описание
    pressure = models.FloatField() #давление, гектопаскали
    humidity = models.IntegerField() #влажность, проценты

    def __str__(self):
        return str(self.city) + "_" + str(self.date)

    class Meta:
        ordering = ['city', 'date']
        verbose_name = "Request"
        verbose_name_plural = "Requests"