from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('products/', views.Products.as_view(), name='all_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category_list'),
]