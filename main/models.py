from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=
                             'products', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    is_official_store = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for foreign keys preparation
    brand_id = models.UUIDField(null=True, blank=True)
    category_id = models.UUIDField(null=True, blank=True)
    shop_id = models.UUIDField(null=True, blank=True)
    seo_keywords_ids = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.name