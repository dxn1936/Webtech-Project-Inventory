from django.contrib import admin
from .models import * 

# Register your models here.


admin.site.register(Category)
admin.site.register(Warehouse)
admin.site.register(Products)
admin.site.register(Product_items_details)
