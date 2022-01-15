from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

# Create your models here.


class SubCategory(models.Model):
    category = models.CharField(unique=True, max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.category


class Category(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.category

    def __unicode__(self):
        return self.category


class Size(models.Model):
    size = models.CharField(max_length=20)

    class Meta:
        ordering = ['size']

    def __unicode__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=32)

    class Meta:
        ordering = ['color']

    def __unicode__(self):
        return self.color


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, null=True, related_name="Subcategory", on_delete=models.SET_NULL)
    name = models.CharField(max_length=40)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ManyToManyField('Size')
    color = models.ManyToManyField('Color')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def tag_category(self):
        return f'{self.category.category}'

    def tag_subcategory(self):
        return f'{self.subcategory.category}'


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=True)
    image = models.ImageField(upload_to="images")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Stock(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    barcode = models.ImageField(upload_to='barcodes/', blank=True)
    unique_together = ('product', 'size', 'color', 'barcode')
    active = models.BooleanField(default=True)

    def tag_product(self):
        return f'{self.product.name}'

    def tag_size(self):
        return f'{self.size.size}'

    def tag_color(self):
        return f'{self.color.color}'

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(
            f'{91}{111100000}{int(self.product.id)}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.id}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
