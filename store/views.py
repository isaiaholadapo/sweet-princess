from django.shortcuts import render, get_object_or_404
from django.views import generic

from . import models


# Create your views here.


class Products(generic.ListView):
    model = models.Product
    template_name = 'store/all_products.html'

    def get_queryset(self):
        queryset = models.Product.products.all()
        return queryset


class ProductDetailView(generic.DetailView):
    template_name = 'store/product_detail.html'

    def get_object(self, queryset=None):
        _slug = self.kwargs.get('slug')
        queryset = get_object_or_404(models.Product, slug=_slug, in_stock=True)
        return queryset


class CategoryListView(generic.ListView):
    template_name = 'store/category.html'

    def get_queryset(self):
        _slug = self.kwargs.get('slug')
        category = get_object_or_404(models.Category, slug=_slug)
        products = models.Product.objects.filter(category__slug=_slug)
        context = {
            "categories": category,
            'products': products
        }
        return context






