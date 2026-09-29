from django.urls import path

from apps.carts.api.v1.views import (
    CartDetailView,
    CartItemAdminManagerView,
    CartItemDetailView,
    CartItemView,
    CartView,
)

urlpatterns = [
    path("", CartView.as_view()),
    path("<int:pk>/", CartDetailView.as_view()),
    path("cart_items_admin_manager/<int:pk>/", CartItemAdminManagerView.as_view()),
    path("cart_items/", CartItemView.as_view()),
    path("cart_items/<int:pk>/", CartItemDetailView.as_view()),
]
