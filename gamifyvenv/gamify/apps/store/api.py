import json
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from apps.cart.cart import Cart


from apps.order.utils import checkout

from .models import Product
from apps.order.models import Order, LibraryItem
from apps.userprofile.views import library


def create_checkout_session(request):
    cart = Cart(request)

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    items = []

    for item in cart:
        product = item['product']

        obj = {
            'price_data': {
                'currency': 'eur',
                'product_data':{
                    'name': product.title
                },
                'unit_amount': int(product.price * 100)
            },
            'quantity': item['quantity']
        }

        items.append(obj)
        
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )
    # Create order
    
    data = json.loads(request.body)
    username = data['username']
    payment_id = session.id
    orderid = checkout(request, username)

    order = Order.objects.get(pk=orderid)
    order.payment_id = payment_id
    order.paid_amount = cart.get_total_cost()
    order.save()
    #

    return JsonResponse({'session': session})



def api_checkout(request):
    cart = Cart(request)
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    username = data['username']

    orderid = checkout(request, username)
    
    paid = True

    if paid == True:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()

    return redirect('/')



def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    
    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)


def api_library_load(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    game_title = data['game_title']
    
    request.session['game_title'] = game_title

    return JsonResponse(jsonresponse)

def api_install_or_uninstall(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}

    game_title = data['game_title']

    try:
        library_item = LibraryItem.objects.filter(username=request.user, game__title=game_title)
    except LibraryItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'LibraryItem not found'})

    for item in library_item:
        if (item.installed):
            item.installed = False
            item.save()
        else:
            item.installed = True
            item.save()

    return JsonResponse(jsonresponse)