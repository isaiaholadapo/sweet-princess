import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from store.models import Product
from .cart import Cart


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


class AddCart(generic.TemplateView):
    template_name = 'cart/add_cart.html'

    def post(self, request, **kwargs):
        cart = Cart(request)
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)

        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=product_qty)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        response = JsonResponse({'qty': cart_qty, 'subtotal': cart_total})
        return response


