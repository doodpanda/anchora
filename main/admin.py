from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'user', 'price', 'category', 'is_featured', 'is_official_store', 'is_blacklisted', 'created_at')
	list_filter = ('is_featured', 'is_official_store', 'is_blacklisted', 'category')
	search_fields = ('name', 'description', 'category', 'user__username')
