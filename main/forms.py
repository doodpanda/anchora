from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'discounted_price', 'description', 'thumbnail',
            'category', 'is_featured', 'is_official_store', 'is_blacklisted',
            'brand_id', 'category_id', 'shop_id', 'seo_keywords_ids'
        ]
