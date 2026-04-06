from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'stock_quantity', 'discount', 'created_at')
    search_fields = ('name', 'description')
    list_filter   = ('created_at',)
    ordering      = ('-created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'quantity', 'total_price', 'status', 'order_date')
    list_filter   = ('status', 'order_date')
    ordering      = ('-order_date',)
    readonly_fields = ('order_date',)
