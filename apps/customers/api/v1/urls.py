from django.urls import path

from apps.customers.api.v1.views import CustomerProfileView, CustomerProfileDetailView


urlpatterns = [
    path('', CustomerProfileView.as_view()),
    path('<int:pk>/', CustomerProfileDetailView.as_view()),
]