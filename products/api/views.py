from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from products.models import Product, Category, SubCategory, Size, Color, Image, Stock
from .serializers import CategoryListSerializer, SubCategoryListSerializer, SubCategoryDetailSerializer, SizeListSerializer, ColorListSerializer, ImageListSerializer, ProductListSerializer, ProductDetailSerializer, StockDetailSerializer, StockListSerializer

# Create your views here.


class CategoryListAPIView(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.all()


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategoryDetailSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = SubCategory.objects.all()
    search_fields = ['id', 'category']


class SubCategoryListAPIView(generics.ListCreateAPIView):
    serializer_class = SubCategoryListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = SubCategory.objects.all()


class SubCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategoryDetailSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = SubCategory.objects.all()
    search_fields = ['id', 'category']


class SizeListAPIView(generics.ListCreateAPIView):
    serializer_class = SizeListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Size.objects.all()


class ColorListAPIView(generics.ListCreateAPIView):
    serializer_class = ColorListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Color.objects.all()


class ImageListAPIView(generics.ListCreateAPIView):
    serializer_class = ImageListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Image.objects.all()


class ProductListApiAuthView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()


class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('category', 'subcategory')
    search_fields = ['name', 'category__category', 'subcategory__category']


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('category', 'subcategory')
    search_fields = ['name', 'category__category', 'subcategory__category']


class StockDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StockDetailSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Stock.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('product', 'size', 'amount', 'color', 'active')


class StockListAPIView(generics.ListCreateAPIView):
    serializer_class = StockListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Stock.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('product', 'size', 'amount', 'color', 'active')
