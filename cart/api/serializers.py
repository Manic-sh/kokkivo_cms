from django.db.models import fields
from rest_framework import serializers
from ..models import Cart


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product', 'size', 'color',
                  'quantity', 'price', 'get_cost']


class CartDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'product', 'size', 'color',
                  'quantity', 'price', 'get_cost']
