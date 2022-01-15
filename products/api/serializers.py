from django.db import models
from django.db.models import fields
from rest_framework import serializers
from products.models import Product, Category, SubCategory, Size, Color, Image, Stock


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category']


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category']


class SubCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'description']


class SubCategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'description']


class SizeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ['id', 'size']


class ColorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['id', 'color']


class ImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'product', 'name', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product_detail', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'subcategory', 'tag_subcategory',
                  'category', 'tag_category', 'size', 'color', 'price', 'url']


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description',
                  'price', 'size', 'color', 'category', 'subcategory', 'tag_category', 'tag_subcategory']


class StockListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id', 'product', 'amount',
                  'size', 'color', 'quantity', 'barcode', 'tag_product', 'tag_size', 'tag_color']


class StockDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id', 'product', 'amount',
                  'size', 'color', 'quantity', 'barcode', 'tag_product', 'tag_size', 'tag_color']
