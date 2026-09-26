from django.urls import path

from apps.carts.api.v1.views import CartItemDetailView, CartItemView, CartView

urlpatterns = [
    path('', CartView.as_view()),
    path('cart_items/', CartItemView.as_view()),
    path('cart_items/<int:pk>/', CartItemDetailView.as_view()),
    
]