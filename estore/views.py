from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal
import json
import datetime
from .models import *
from .utils import *


def store(request):
    context = {}
    context['cartItems'] = cartData(request)['cartItems']
    context['products'] = Product.objects.all()
    return render(request, 'estore/store.html', context)

def cart(request):
    context = cartData(request)
    return render(request, 'estore/cart.html', context)

def checkout(request):
    context = cartData(request)
    return render(request, 'estore/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()
        
    return JsonResponse('Item quantity updated', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    
    total = Decimal(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zipcode = data['shipping']['zipcode'],
    )

    return JsonResponse('Payment submitted', safe=False)
