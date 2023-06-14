from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Property(models.Model):
    category = models.ForeignKey(Category, related_name='properties', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    price = models.BigIntegerField()
    image = models.ImageField(upload_to='property_images', default='../static/default_home.jpg', blank=True, null=True)
    for_sale = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    