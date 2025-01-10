from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Transaction
import requests


# Verify payment
def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response_data = response.json()
        if response_data['status'] and response_data['data']['status'] == 'success':
            transaction = Transaction.objects.get(reference=reference)
            transaction.status = 'success'
            transaction.save()
            return render(request, 'payment/payment_success.html', {'transaction': transaction})
        else:
            return render(request, 'payment/payment_failed.html')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Initiate payment
def initiate_payment(request):
    total_price = request.GET.get('total_price')
    email = request.GET.get('email')

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    data = {
        'email': email,
        'amount': int(float(total_price) * 100),  # Paystack expects amount in kobo
    }
    try:
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        response_data = response.json()
        if response_data['status']:
            return redirect(response_data['data']['authorization_url'])
        else:
            return JsonResponse({'error': response_data['message']}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
