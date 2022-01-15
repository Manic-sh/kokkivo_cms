from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (OrderListSerializer, OrderDetailSerializer,
                          OrderItemListSerializer, OrderItemDetailSerializer, PaymentModeSerializer, PaymentSerializer
                          )
from django.db.models import Sum
from django.conf import settings
from ..models import Order, OrderItem, PaymentMode, Payment


@api_view(['GET', 'POST'])
def ApiHomePage(request, format=None):
    return Response({
        'orders': reverse('order_list', request=request, format=format),
        'order-items': reverse('order_item_list', request=request, format=format),
        'product': reverse('product_list', request=request, format=format),
        'subcategories': reverse('subcategory_list', request=request, format=format),
    })


@api_view(['GET'])
def ReportOrderApiView(request, format=None):
    orders = Order.objects.all()
    total_value = 0
    total_orders = orders.count() if orders else 0
    average_order = 0
    return Response({
        'count': total_orders,
        'total': f'{total_value}',
        'avg': f'{average_order}',
    })


class OrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('status', )


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Order.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class OrderItemListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderItemListSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = OrderItem.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ['product', 'order', ]
    search_fields = ['product__name', 'order__user']


class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemDetailSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = OrderItem.objects.all()


class PaymentModeAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentModeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = PaymentMode.objects.all()


class PaymentAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Payment.objects.all()
