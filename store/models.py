from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_create', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/product/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={'slug': self.slug})
