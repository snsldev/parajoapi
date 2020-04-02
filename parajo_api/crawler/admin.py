from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(CarModelDetail)
admin.site.register(CarInfo)