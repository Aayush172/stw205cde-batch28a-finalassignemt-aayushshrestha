from django.db import models
from django.core.validators import *
from django.core import validators


class Category(models.Model):
    category_name = models.CharField(max_length=200, null=True, validators=[validators.MinLengthValidator(2)])
    category_description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name= models.CharField(max_length=50)
    product_price = models.FloatField()
    product_image = models.FileField(upload_to='static/upload')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

