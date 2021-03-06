from __future__ import unicode_literals
from decimal import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Category, Product, Size, Color, Stock
from cart.forms import CartForm


def products_list(request, category_name=None):
    selected_categories = None
    all_products = Product.objects.all()
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if category_name:
        category = get_object_or_404(Category, category=category_name)
        all_products = Product.objects.filter(category=category)
    else:
        category = None

    if request.GET.getlist('category'):
        selected_categories = Category.objects.filter(
            category__in=request.GET.getlist('category'))
        # filter products for selected categories
        all_products = [
            product for product in all_products if product.category in selected_categories]

    if request.GET.getlist('size'):
        # get size objects for selected sizes
        selected_sizes_objects = Size.objects.filter(
            size__in=request.GET.getlist('size'))
        # get sizes strings for selected sizes
        selected_sizes = [size.size for size in selected_sizes_objects]
        # filter products for selected sizes
        all_products = [product for product in all_products if product.size.filter(
            size__in=selected_sizes)]

    if request.GET.getlist('color'):
        # get color objects for selected colors
        selected_color_objects = Color.objects.filter(
            color__in=request.GET.getlist('color'))
        # get color strings for selected colors
        selected_colors = [color.color for color in selected_color_objects]
        # filter products for selected colors
        all_products = [product for product in all_products if product.color.filter(
            color__in=selected_colors)]

    if request.GET.getlist('start_price') and request.GET.getlist('end_price'):
        # convert start and end prices to decimals
        start_price = Decimal(request.GET.getlist('start_price')[0])
        end_price = Decimal(request.GET.getlist('end_price')[0])
        # filter products by selected price range
        all_products = [product for product in all_products if product.price >=
                        start_price and product.price <= end_price]

    # filter products which are in stock
    products_in_stock = list(set(
        [product for product in all_products for stock in product.stock_set.all() if stock.amount > 0]))
    # create a list of products, each item is a dictionary with product object and image object
    products_list = [dict(product=product, image=product.image_set.all()[
                          0]) for product in products_in_stock]

    # sort products by new in by default
    products_sorted = sorted(
        products_list, key=lambda k: k['product'].created, reverse=True)

    if request.GET.getlist('sort'):
        if 'low-to-high' in request.GET.getlist('sort'):
            # sort products by price low to high
            products_sorted = sorted(
                products_list, key=lambda k: k['product'].price)
        if 'high-to-low' in request.GET.getlist('sort'):
            # sort products by price high to low
            products_sorted = sorted(
                products_list, key=lambda k: k['product'].price, reverse=True)

    # Show certain amount of products per page
    paginator = Paginator(products_sorted, 8)

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    pages_range = paginator.page_range
    try:
        current_page = int(page)
    except Exception as e:
        current_page = 1

    args = {
        'selected_categories': selected_categories,
        'products': products,
        'categories': categories,
        'category': category,
        'sizes': sizes,
        'colors': colors,
        'current_page': current_page,
        'pages_range': pages_range
    }

    # in case of ajax call update products html
    if request.is_ajax():
        html = render_to_string(
            'products/filtered_products.html', {'products': products})
        return HttpResponse(html)

    return render(request, 'products/products_list.html', args)


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    images = product.image_set.all()
    sizes = product.size.all()
    # filter stock where amount is more than 0 for the selected product
    stock = Stock.objects.filter(product=product, amount__gt=0)
    # get available sizes for the product, remove duplicates and sort by size field
    sizes_available = sorted(
        set([item.size for item in stock]), key=lambda k: k.size)
    cart_form = CartForm()

    args = {'product': product, 'images': images, 'sizes': sizes,
            'sizes_available': sizes_available, 'cart_form': cart_form}

    return render(request, 'products/product.html', args)
