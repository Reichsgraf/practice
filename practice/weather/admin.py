from weather.models import *
from django.contrib import admin

class WeatherInline(admin.TabularInline):
    model = Request

class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    inlines = [WeatherInline]

    class Meta:
        model = City
admin.site.register(City, CityAdmin)

class CloudsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cloud._meta.fields]

    class Meta:
        model = Cloud
admin.site.register(Cloud, CloudsAdmin)

class RequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Request._meta.fields]

    class Meta:
        model = Request
admin.site.register(Request, RequestAdmin)