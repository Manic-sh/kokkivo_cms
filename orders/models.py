# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from typing import Callable

from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

from products.models import Product, Size, Color


class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=40, null=True)
    postcode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='Processing', max_length=20)

    class Meta:
        ordering = ('-created',)

    def get_subtotal_cost(self):
        return '{0:.2f}'.format(sum(item.get_cost() for item in self.items.all()))

    def get_delivery_cost(self):
        if Decimal(self.get_subtotal_cost()) > Decimal(75.00):
            return '{0:.2f}'.format(0)
        else:
            return '{0:.2f}'.format(2.95)

    def get_total_cost(self):
        return '{0:.2f}'.format(Decimal(self.get_subtotal_cost()) + Decimal(self.get_delivery_cost()))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity


class PaymentMode(models.Model):
    """Payment option available"""
    name = models.CharField(unique=True, max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled')
    )
    order = models.ForeignKey(
        Order, related_name='order', on_delete=models.CASCADE)
    paymode = models.ForeignKey(
        PaymentMode, on_delete=models.SET_NULL, null=True)
    paystatus = models.CharField(
        choices=PAYMENT_STATUS_CHOICES, default="Completed", max_length=20)

    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_payment_status(self):
        return f'{self.paystatus}'
