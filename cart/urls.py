from django.urls import path

from . import views
from .cart import Cart

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name='cart'),
    path('add/', views.AddCart.as_view(), name='add_cart'),
    path('delete', views.cart_delete, name='cart-delete'),
    path('update', views.cart_update, name='cart-update'),
]
