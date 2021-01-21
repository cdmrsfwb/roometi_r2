import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_no_of_items': 0}
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = product.price * cart[i]
            order['get_cart_total'] += total
            order['get_no_of_items'] += cart[i]
            items.append({
                'product': product,
                'quantity': cart[i],
                'get_total': total,
            })
        except:
            pass
    cartItems = order['get_no_of_items']
    
    return {'items': items, 'order': order, 'cartItems': cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_no_of_items
        context = {'items': items, 'order': order, 'cartItems': cartItems}
    else:
        context = cookieCart(request)
    return context

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    items = cookieCart(request)['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        orderItem = OrderItem.objects.create(product=item['product'], order=order, quantity=item['quantity'])
    return customer, order
