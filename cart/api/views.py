from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (CartListSerializer, CartDetailSerializer)
from products.models import Product
from ..models import Cart


class CartItemListAPIView(generics.ListCreateAPIView):
    serializer_class = CartListSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Cart.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ['product', 'size', 'color']


class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartDetailSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Cart.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ['product', 'size', 'color']


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # get product object by id
    product = get_object_or_404(Product, id=product_id)
    # get selected size from request data
    size = request.POST['size']
    updated_cart = cart.add(product=product, size=size, quantity=1,
                            update=True)
    if updated_cart:
        # if cart updated return success status
        subtotal_price = cart.get_subtotal_price()
        delivery_price = cart.get_delivery_price()
        total_price = cart.get_total_price()
        data = {
            'subtotal_price': subtotal_price,
            'delivery_price': delivery_price,
            'total_price': total_price
        }
        return JsonResponse(data, status=200)
