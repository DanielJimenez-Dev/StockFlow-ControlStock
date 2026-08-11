from django.contrib import admin
from .models import Category, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'current_stock', 'min_stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('sku', 'name')
    list_editable = ('price', 'current_stock')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'user', 'created_at')
    list_filter = ('movement_type', 'created_at')
