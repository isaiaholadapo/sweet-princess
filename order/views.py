import json

from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from cart.cart import Cart
from .forms import OrderForm

from .models import Order, OrderItem


def add_order(request):
    cart = Cart(request)
    print('testing')
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            print('posttt')
            order_key = 34324
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            user_id = request.user.id
            cart_total = cart.get_total_price()
            print(state)

            # Check if order exists
            # if Order.objects.filter(order_key=order_key).exists():
            #     pass
            # else:
            order = Order.objects.create(user=user_id, first_name=first_name, last_name=last_name, address1=address,
                                         phone=phone, state=state, total_paid=cart_total, order_key=order_key)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

            response = JsonResponse({'success': 'Return something'})
            return response
    else:
        print('not posted')
        return 'failed'


class VoteUpPost(generic.CreateView):
    form_class = OrderForm
    success_url = reverse_lazy('account:dashboard')

    def form_valid(self, form):
        cart = Cart(self.request)
        order_key = 34324
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        phone = self.request.POST.get('phone')
        address = self.request.POST.get('address')
        state = self.request.POST.get('state')
        user_id = self.request.user.id
        cart_total = cart.get_total_price()
        print(state)

        # Check if order exists
        # if Order.objects.filter(order_key=order_key).exists():
        #     pass
        # else:
        order = Order.objects.create(user=user_id, first_name=first_name, last_name=last_name, address1=address,
                                     phone=phone, state=state, total_paid=cart_total, order_key=order_key)
        order_id = order.pk

        for item in cart:
            OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response

    def form_invalid(self, form):
        print('fomr invalid')
        return self.render_to_response(self.get_context_data(form=form))


def create_order_view(request):
    cart = Cart(request)
    if request.POST.get('action') == 'create_order':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address1 = request.POST.get('address1')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        total_paid = cart.get_total_price()
        order_key = 45345

        Order.objects.create(
            user=user, first_name=first_name, last_name=last_name, address1=address1, state=state, phone=phone,
            total_paid=total_paid, order_key=order_key
        )

    response = JsonResponse({'success': 'Return something'})
    return render(request, 'order/index.html')


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
