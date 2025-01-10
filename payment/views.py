from django.shortcuts import get_object_or_404
from .models import Transaction
import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from store.models import Dress


def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response_data = response.json()
        if response_data['status'] and response_data['data']['status'] == 'success':
            # Mark the transaction as successful in the database
            transaction = Transaction.objects.get(reference=reference)
            transaction.status = 'success'
            transaction.save()
            return render(request, 'payment/payment_success.html', {'transaction': transaction})
        else:
            return render(request, 'payment/payment_failed.html')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def initiate_payment(request, dress_id):
    dress = get_object_or_404(Dress, id=dress_id)  # Fetch the dress
    if request.method == 'POST':
        email = request.POST['email']
        amount = int(dress.price * 100)  
        transaction = Transaction.objects.create(amount=amount, email=email)
        
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'amount': amount,
            'reference': str(transaction.reference),  # Convert UUID to string
            'callback_url': 'http://127.0.0.1:8000/payment/verify-payment/',  # Adjust as necessary
        }
        
        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))
            response_data = response.json()
            
            if response_data['status']:
                # Redirect to Paystack payment page
                authorization_url = response_data['data']['authorization_url']
                return redirect(authorization_url)
            else:
                return JsonResponse({'error': 'Payment initialization failed.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'payment/initiate_payment.html', {'dress': dress})

def initiate_cart_payment(request, total_price, email):
    try:
        amount = int(float(total_price) * 100)  
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
            'callback_url': 'http://127.0.0.1:8000/payment/verify-payment/',  
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