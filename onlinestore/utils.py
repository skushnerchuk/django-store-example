from time import time

from django.utils.text import slugify
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator


class ObjectCreateMixin:
    """Общий функционал в создании объектов"""
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bounded_form = self.form_model(request.POST, request.FILES)
        if bounded_form.is_valid():
            new_obj = bounded_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bounded_form})


class ObjectEditMixin:
    """Общий функционал в редактировании объектов"""
    form_model = None
    model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bounded_form = self.form_model(instance=obj)
        return render(request, self.template,
                      context={'form': bounded_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bounded_form = self.form_model(request.POST, instance=obj)

        if bounded_form.is_valid():
            updated_obj = bounded_form.save()
            return redirect(updated_obj)
        return render(request, self.template,
                      contect={'form': bounded_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    """Общий функционал в удалении объектов"""
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


class SlugMixin:
    """Миксин для формирования slug-полей в объектах"""

    @staticmethod
    def gen_slug(s):
        """Генерация случайного slug для идентификации объекта"""
        new_slug = slugify(s, allow_unicode=True)
        return '{}-{}'.format(new_slug, int(time()))

    def save(self, *args, **kwargs):
        # Делаем так, что slug автоматически создается только для новых объектов
        if not self.id:
            self.slug = self.gen_slug(self.name)
        super().save(*args, **kwargs)


class PaginatorMixin:
    """Общий функционал в создании постраничной навигации"""

    @staticmethod
    def create_paginator(request, objects, objects_num):
        paginator = Paginator(objects, objects_num)
        page_num = request.GET.get('page', 1)
        page = paginator.get_page(page_num)

        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        return {
            'paginator': paginator,
            'page': page,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url
        }
