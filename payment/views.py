# payment/views.py
from django.shortcuts import render
from django.http import JsonResponse
from store.models import Dress
from .models import Transaction
import json
import requests
from django.conf import settings

def initiate_cart_payment(request, total_price, email):
    try:
        amount = int(float(total_price) * 100)  # Convert to kobo (NGN cents)
        transaction = Transaction.objects.create(amount=amount, email=email)
        
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'email': email,
            'amount': amount,
            'reference': str(transaction.reference),
            'callback_url': 'http://127.0.0.1:8000/payment/verify-payment/',  # Adjust for production URL
        }

        # Request to Paystack API to initialize payment
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response_data['status']:
            # Redirect to Paystack's payment page
            authorization_url = response_data['data']['authorization_url']
            return redirect(authorization_url)
        else:
            return JsonResponse({'error': 'Payment initialization failed.'}, status=500)

    except ValueError:
        return JsonResponse({'error': 'Invalid total price format.'}, status=400)
