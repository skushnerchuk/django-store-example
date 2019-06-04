from django.contrib import admin
from .models import Product, Category

# Регистрируем модели для редактирования/добавления/удаления данных через штатную админку
admin.site.register(Category)
admin.site.register(Product)
