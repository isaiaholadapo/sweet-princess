import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings

from pypaystack import Transaction, Customer, Plan


from cart.cart import Cart

# Create your views here.

def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required()
def cart_view(request):
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    context = {
        'client_secret': settings.PAYSTACK_PUBLIC_KEY,
        "user": request.user,
        "total": total,
    }
    return render(request, 'payment/home.html', context=context)


def verify_transaction(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    print('verify')
    return data

