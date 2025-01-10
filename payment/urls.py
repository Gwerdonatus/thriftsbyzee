from django.urls import path
from . import views


urlpatterns = [
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
]
