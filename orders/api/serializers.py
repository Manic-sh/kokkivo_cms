from django.db.models import fields
from rest_framework import serializers
from ..models import Order, OrderItem, Payment, PaymentMode


class OrderListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='order_detail', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'phone', 'created',
                  'updated', 'status', 'get_subtotal_cost', 'get_delivery_cost', 'get_total_cost', 'url']


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'address', 'phone', 'created', 'updated', 'status',
                  'get_subtotal_cost', 'get_delivery_cost', 'get_total_cost']


class OrderItemListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='order_item_detail', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product',
                  'size', 'price', 'quantity', 'get_cost', 'url']


class OrderItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product',
                  'size', 'price', 'quantity', 'get_cost']


class PaymentModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMode
        fields = ['id', 'name']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'paymode', 'paystatus', 'updated']
