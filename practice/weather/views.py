from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from weather.models import *
from weather.forms import *
from lxml import etree
import requests
import datetime

def xml_parsing(xml_file, index): #XML-результат содержит больше (полезной) информации, чем JSON, потому вот.
    path = '/weatherdata/forecast/time[@day="' + index + '"]'
    date = datetime.datetime.strptime(index, "20%y-%m-%d").date()
    date.strftime("%B %d, %Y")
    temp_min = xml_file.xpath(path + '/temperature')[0].get('min')
    temp_min = int(round(float(temp_min) - 273.15, 1)) #минимальная температура в градусах Цельсия
    temp_max = xml_file.xpath(path + '/temperature')[0].get('max')
    temp_max = int(round(float(temp_max) - 273.15, 1)) #максимальная температура в градусах Цельсия

    description = xml_file.xpath(path + '/symbol')[0].get('name') #облачность, описание
    image = xml_file.xpath(path + '/symbol')[0].get('var') #облачность, изображение
    if Cloud.objects.filter(cloud_id=image).exists():
        cloudiness = Cloud.objects.get(cloud_id=image)
    else:
        image="0d"
        cloudiness = Cloud.objects.get(cloud_id=image) #не все изображения есть в наличие, потому используется заглушка

    pressure = xml_file.xpath(path + '/pressure')[0].get('value') #давление, в гектопаскалях (hPa)
    humidity = xml_file.xpath(path + '/humidity')[0].get('value') #влажность, в процентах

    wind_degree = xml_file.xpath(path + '/windDirection')[0].get('deg') #направление ветра, градусы
    wind_direction = xml_file.xpath(path + '/windDirection')[0].get('name') #направление ветра, описание

    wind_speed = xml_file.xpath(path + '/windSpeed')[0].get('mps') #скорость ветра, метры в секунду
    wind_description = xml_file.xpath(path + '/windSpeed')[0].get('name') #скорость ветра, описание

    return date, description, cloudiness, temp_min, temp_max, pressure, humidity, \
           wind_degree, wind_direction, wind_speed, wind_description

def xml_request(form, city_name, request_days):
    request_weather = []
    # cnt=6 по той причине, что тестировалось в 1:00 и вместо нового дня API выводила предыдущий.
    # Вывод API шести дней позволяет избежать этой ошибки.
    tree = etree.parse("http://api.openweathermap.org/data/2.5/forecast/daily?q=" + city_name
                       + "&cnt=6&id=524901&APPID=e9e93af54962988557feeaec022fec6b&mode=xml")
    city_true_name = tree.xpath('/weatherdata/location/name')[0].text
    if not City.objects.filter(city=city_name).exists():
        coord_lat = tree.xpath('/weatherdata/location/location')[0].get('latitude')
        coord_lon = tree.xpath('/weatherdata/location/location')[0].get('longitude')
        city = City.objects.create(city=city_true_name, coord_lon=coord_lon, coord_lat=coord_lat)
        city.save()
    else:
        city = City.objects.get(city=city_name)
    for day in request_days:
        # date, description, image, temp_min, temp_max, pressure, humidity, wind_degree, wind_direction, wind_speed, wind_description
        xml_weather = xml_parsing(tree, day)
        request_weather.append(dict([('date', xml_weather[0]), ('description', xml_weather[1]), ('cloudiness', xml_weather[2]),
                                     ('temp_min', xml_weather[3]), ('temp_max', xml_weather[4]), ('pressure', xml_weather[5]),
                                     ('humidity', xml_weather[6]), ('wind_degree', xml_weather[7]), ('wind_direction', xml_weather[8]),
                                     ('wind_speed', xml_weather[9]), ('wind_description', xml_weather[10])]))
        request_to_db, create = Request.objects.get_or_create(city=city, date=xml_weather[0],
                                                              description=xml_weather[1],
                                                              cloudiness=xml_weather[2], temp_min=xml_weather[3],
                                                              temp_max=xml_weather[4],
                                                              pressure=xml_weather[5], humidity=xml_weather[6],
                                                              wind_degree=xml_weather[7],
                                                              wind_direction=xml_weather[8], wind_speed=xml_weather[9],
                                                              wind_description=xml_weather[10])
        request_to_db.save()
    context = {
        'form': form,
        'city': city_true_name,
        'weather_list': request_weather,
        'notes': "The information was taken from the application.",
    }
    return context

def db_request(form, request_city, request_days):
    request_weather = []
    for day in request_days:
        request_weather.append(Request.objects.get(city=request_city, date=day))
    context = {
        'form': form,
        'city': request_city,
        'weather_list': request_weather,
        'notes': "The information was taken from the data base.",
    }
    return context

def weather(request):
   request_days = []
   API_source = True
   for day in range(5):
        today = datetime.date.today()
        delta = datetime.timedelta(days=day)
        nextday = today + delta
        request_days.append(nextday.strftime('20%y-%m-%d'))
   form = CityForm(request.POST or None)
   if request.method == "POST" and form.is_valid():
        request_text = form.cleaned_data
        city_name = request_text["city"]
        form = CityForm()
        if City.objects.filter(city=city_name).exists():
            request_city = City.objects.get(city=city_name)
            for day in request_days:
                if Request.objects.filter(city=request_city, date=day).exists():
                    API_source = False
                else:
                    API_source = True
                    break
        if API_source:
            context = xml_request(form, city_name, request_days)
        else:
            context = db_request(form, request_city, request_days)
        return render(request, "weather/weather.html", context)
   context = {
        'city': "None",
        'notes': "Error. Try again or сheck name of the city",
   }
   return render(request, "weather/weather.html", context)