from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'
        })

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'
        })

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'discounted_price', 'description', 'thumbnail',
            'category', 'is_featured', 'is_official_store', 'is_blacklisted',
            'brand_id', 'category_id', 'shop_id', 'seo_keywords_ids'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent resize-vertical', 'rows': 4}),
            'thumbnail': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'category': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'rounded border-ash_gray-300 text-shamrock_green focus:ring-shamrock_green'}),
            'is_official_store': forms.CheckboxInput(attrs={'class': 'rounded border-ash_gray-300 text-shamrock_green focus:ring-shamrock_green'}),
            'is_blacklisted': forms.CheckboxInput(attrs={'class': 'rounded border-ash_gray-300 text-red-600 focus:ring-red-500'}),
            'brand_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'category_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'shop_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
            'seo_keywords_ids': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-ash_gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-shamrock_green focus:border-transparent'}),
        }
