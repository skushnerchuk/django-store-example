from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Category, Product
from .forms import CategoryForm, ProductForm
from .utils import ObjectCreateMixin, ObjectEditMixin, ObjectDeleteMixin, PaginatorMixin


class AllProducts(PaginatorMixin, View):
    """Вывод списка всех продуктов без учета категорий"""

    def get(self, request):
        search_query = request.GET.get('search', '')
        categories = Category.objects.all()
        if search_query:
            cond = Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(short_description__icontains=search_query)
            products = Product.objects.filter(cond)
        else:
            products = Product.objects.all()
        paginator = self.create_paginator(request, products, 6)
        context = {
            'category': categories,
            'page_object': paginator['page'],
            'is_paginated': paginator['is_paginated'],
            'next_url': paginator['next_url'],
            'prev_url': paginator['prev_url'],
        }
        return render(request, 'onlinestore/index.html', context=context)


class Cart(View):
    """Вывод содержимого корзины"""

    @staticmethod
    def create_cart(request):
        cart_items = []
        total_amount = 0
        # Формируем данные для таблицы заказа
        for item in request.session['cart']:
            product = Product.objects.filter(slug=item)[0]
            total_amount += product.price * request.session['cart'][item]
            cart_items.append({
                'name': product.name,
                'count': request.session['cart'][item],
                'price': product.price,
                'id': product.slug
            })
        return cart_items, total_amount

    def get(self, request):
        if 'cart' not in request.session:
            return render(request, 'onlinestore/cart.html', context={})
        cart_items, total_amount = self.create_cart(request)
        return render(request, 'onlinestore/cart.html', context={'cart': cart_items, 'total': total_amount})

    def post(self, request):
        if 'reset' in request.POST:
            request.session.clear()
            return redirect('/', 302)
        if 'delete' in request.POST and request.POST['id'] in request.session['cart']:
            del request.session['cart'][str(request.POST['id'])]
            return redirect('/cart', 302)
        cart_items, total_amount = self.create_cart(request)
        return render(request, 'onlinestore/cart.html', context={'cart': cart_items, 'total': total_amount})


class ProductsByCategory(PaginatorMixin, View):
    """Вывод списка всех продуктов по категории"""

    def get(self, request, slug):
        categories = []
        paginator = None

        try:
            categories = Category.objects.all()
            products = Product.objects.filter(category__slug=slug)
            paginator = self.create_paginator(request, products, 6)
        except ObjectDoesNotExist:
            pass

        context = {
            'category': categories,
            'page_object': paginator['page'],
            'is_paginated': paginator['is_paginated'],
            'next_url': paginator['next_url'],
            'prev_url': paginator['prev_url'],
        }

        return render(request, 'onlinestore/index.html', context=context)


class ProductDetail(View):
    """Вывод сведений по продукту"""

    @staticmethod
    def add_product_to_session(request, product_slug):
        if 'cart' not in request.session:
            request.session['cart'] = {}
        if product_slug in request.session['cart']:
            request.session['cart'][product_slug] += 1
        else:
            request.session['cart'][product_slug] = 1

    @staticmethod
    def get(request, slug):
        product = None
        categories = []

        try:
            categories = Category.objects.all()
            product = get_object_or_404(Product, slug__iexact=slug)
        except ObjectDoesNotExist:
            pass

        context = {
            'category': categories,
            'product': product,
            'admin_object': product,
            'detail': True
        }
        return render(request, 'onlinestore/product_detail.html', context=context)

    def post(self, request, slug):
        obj = Product.objects.get(slug__iexact=slug)
        self.add_product_to_session(request, slug)
        return redirect(obj)


class CategoryCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """Создание категорий"""
    form_model = CategoryForm
    template = 'onlinestore/category_create.html'
    raise_exception = True


class ProductCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """Создание продуктов"""
    form_model = ProductForm
    template = 'onlinestore/product_create.html'
    raise_exception = True


class CategoryEdit(LoginRequiredMixin, ObjectEditMixin, View):
    """Редактирование категорий"""
    model = Category
    form_model = CategoryForm
    template = 'onlinestore/category_update.html'
    raise_exception = True


class ProductEdit(LoginRequiredMixin, ObjectEditMixin, View):
    """Редактирование продуктов"""
    model = Product
    form_model = ProductForm
    template = 'onlinestore/product_update.html'
    raise_exception = True


class CategoryDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """Удаление категорий"""
    model = Category
    template = 'onlinestore/delete_category.html'
    redirect_url = 'all_products_url'
    raise_exception = True


class ProductDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """Удаление продуктов"""
    model = Product
    template = 'onlinestore/delete_product.html'
    redirect_url = 'all_products_url'
    raise_exception = True
