from django.shortcuts import render, redirect

from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.thumbnail.url, url)

        productsstring = productsstring + b
    
    context = {
        'cart': cart,
        'productsstring': productsstring
    }

    return render(request, 'cart.html', context)