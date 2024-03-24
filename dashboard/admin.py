from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group
# Register your models here.
admin.site.site_header = "Agniv's Inventory Dashboard"

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','quantity', 'buying_price', 'selling_price')
    list_filter=['category']
    fields=('name','category','quantity','buying_price','selling_price')
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
