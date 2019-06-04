from django.urls import path

from .views import AllProducts, Cart, CategoryCreate, ProductsByCategory, CategoryEdit, \
    CategoryDelete, ProductCreate, ProductDetail, ProductEdit, ProductDelete

urlpatterns = [
    path('', AllProducts.as_view(), name='all_products_url'),
    path('cart/', Cart.as_view(), name='cart_url'),
    path('category/create/', CategoryCreate.as_view(), name='create_category_url'),
    path('category/<str:slug>/', ProductsByCategory.as_view(), name='products_by_category'),
    path('category/<str:slug>/edit/', CategoryEdit.as_view(), name='edit_category_url'),
    path('category/<str:slug>/delete/', CategoryDelete.as_view(), name='delete_category_url'),

    path('product/create/', ProductCreate.as_view(), name='product_create_url'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<str:slug>/edit/', ProductEdit.as_view(), name='product_edit_url'),
    path('product/<str:slug>/delete/', ProductDelete.as_view(), name='delete_product_url'),
]
