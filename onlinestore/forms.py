from django import forms
from .models import Category, Product
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    """Форма для работы с категориями (альтернатива админке)"""

    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be a "create"')
        if Category.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug'.format(new_slug))
        return new_slug


class ProductForm(forms.ModelForm):
    """Форма для работы с продуктами (альтернатива админке)"""

    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'short_description', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be a "create"')
        return new_slug
