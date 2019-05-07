
# Create your models here.
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories", blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products", blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    brand = models.CharField(max_length=200, blank=True)
    shipping = models.TextField(blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
    def toDict(self):
        return {
            'Category':self.category,
            'Title':self.title,
            'Price':self.price,
            'Brand':self.brand
        }

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=5)
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

class Contact(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone_number = models.IntegerField(max_length=255, blank=True)
    message = models.TextField(blank=True)

    def toDict(self):
        return {
            'full_name': self.full_name,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'message': self.message
        }
    def __str__(self):
        return self.full_name