from django.urls import path
from . import views

urlpatterns = [
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('initiate-payment/<int:dress_id>/', views.initiate_payment, name='initiate_payment'),
    path('initiate-cart-payment/<slug:total_price>/<email>/', views.initiate_cart_payment, name='initiate_cart_payment'),

]