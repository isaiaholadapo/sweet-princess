from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('verify/<str:id>', views.verify_transaction, name='verify'),
    path('order-placed/', views.order_placed, name='order_placed'),

]
