from django.shortcuts import render, get_object_or_404, redirect
from .models import Dress
from django.contrib import messages
from decimal import Decimal
from django.urls import reverse


# Main store page
def dress_list(request):
    dresses = Dress.objects.all()
    return render(request, 'store/dress_list.html', {'dresses': dresses})


# Dress detail page
def dress_detail(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)
    return render(request, 'store/dress_detail.html', {'dress': dress})


def add_to_cart(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)
    cart = request.session.get('cart', {})

    if str(dress_id) in cart:
        messages.info(request, f"{dress.name} is already in your cart.")
    else:
        cart[str(dress_id)] = {
            'name': dress.name,
            'price': float(dress.price),
            'size': dress.size,
            'quantity': 1,
        }
        messages.success(request, f"{dress.name} added to cart.")

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'store/cart.html', {'cart': cart})


def checkout(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        email = request.POST['email']
        total_price_str = str(int(total_price)) if total_price.is_integer() else f"{total_price:.2f}"
        return redirect('initiate_cart_payment', total_price=total_price_str, email=email)

    return render(request, 'store/checkout.html', {'cart': cart, 'total_price': total_price})


