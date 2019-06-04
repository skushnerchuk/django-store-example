import os

from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse

from . utils import SlugMixin


def validate_file_extension(value):
    """Валидатор расширений загружаемых файлов"""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Category(SlugMixin, models.Model):
    """Категории продуктов"""
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    # Вспомогательные методы, используемые в шаблонах для формирования ссылок
    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('edit_category_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_category_url', kwargs={'slug': self.slug})


class Product(SlugMixin, models.Model):
    """Продукт"""
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=150, unique=True)
    image = models.FileField(upload_to='static/images', validators=[validate_file_extension])
    price = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    short_description = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    # Вспомогательные методы, используемые в шаблонах для формирования ссылок
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('product_edit_url', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.image.name

    def get_delete_url(self):
        return reverse('delete_product_url', kwargs={'slug': self.slug})
