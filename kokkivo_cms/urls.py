"""kokkivo_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.api.views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView, SizeListAPIView, ColorListAPIView, ImageListAPIView, StockDetailAPIView, StockListAPIView
from orders.api.views import OrderListAPIView, OrderDetailAPIView, OrderItemListAPIView, OrderItemDetailAPIView, ReportOrderApiView, PaymentModeAPIView, PaymentAPIView
from cart.api.views import CartItemListAPIView, CartItemDetailAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("accounts.urls")),
    path("cart/", include("cart.urls")),

    path('api/product-list/', ProductListAPIView.as_view(), name='product_list'),
    path('api/product-detail/<int:pk>/',
         ProductDetailAPIView.as_view(), name='product_detail'),
    path('api/category-list/', CategoryListAPIView.as_view(), name='category_list'),
    path('api/subcategory-list/', SubCategoryListAPIView.as_view(),
         name='subcategory_list'),
    path('api/subcategory-detail/<int:pk>/', SubCategoryDetailAPIView.as_view(),
         name='subcategory_Detail'),
    path('api/size-list/', SizeListAPIView.as_view(), name='size-list'),
    path('api/color-list/', ColorListAPIView.as_view(), name='color-list'),
    path('api/image-list/', ImageListAPIView.as_view(), name='image-list'),
    path('api/stock-detail/<int:pk>/',
         StockDetailAPIView.as_view(), name='stock-detail'),
    path('api/stock-list/', StockListAPIView.as_view(), name='stock-list'),

    path('api/order-list/', OrderListAPIView.as_view(), name='order_list'),
    path('api/order-detail/<int:pk>/',
         OrderDetailAPIView.as_view(), name='order_detail'),
    path('api/order-item-list/', OrderItemListAPIView.as_view(),
         name='order_item_list'),
    path('api/order-item-detail/<int:pk>/',
         OrderItemDetailAPIView.as_view(), name='order_item_detail'),
    path('api/payment-mode/', PaymentModeAPIView.as_view(), name='payment-mode'),
    path('api/orders/reports/', ReportOrderApiView),

    path('api/cart-item-list/', CartItemListAPIView.as_view(), name='cart_detail'),
    path('api/cart-item-detail/<int:pk>/',
         CartItemDetailAPIView.as_view(), name='cart_add'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
