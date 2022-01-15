# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order, OrderItem, PaymentMode, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'phone', 'status',
                    'created', 'updated']
    list_filter = ['status', 'created', 'updated']


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'size', 'price', 'quantity']
    list_filter = ['product__name']


admin.site.register(OrderItem, OrderItemAdmin)


class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['active']


admin.site.register(PaymentMode, PaymentModeAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'paymode', 'paystatus', 'updated']
