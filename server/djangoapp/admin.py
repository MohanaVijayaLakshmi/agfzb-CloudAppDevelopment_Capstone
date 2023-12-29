from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake

# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ["make", "name", "dealer_id", "car_type", "year"]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ["name", "description"]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)