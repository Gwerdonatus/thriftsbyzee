from django.urls import path
from . import views
from payment import views as payment_views 

urlpatterns = [
    path('dress-list/', views.dress_list, name='dress_list'),
    path('dress/<int:dress_id>/', views.dress_detail, name='dress_detail'),
    path('add-to-cart/<int:dress_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('initiate-cart-payment/<str:total_price>/<str:email>/', payment_views.initiate_cart_payment, name='initiate_cart_payment'),
]
