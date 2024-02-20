from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

class CarModelInline(admin.TabularInline):
    model = CarModel

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')

# Register models here
