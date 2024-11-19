from django.urls import path
from . import views

urlpatterns = [
    path('', views.dress_list, name='dress_list'),
    path('<int:dress_id>/', views.dress_detail, name='dress_detail'),
    path('add-to-cart/<int:dress_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
]

