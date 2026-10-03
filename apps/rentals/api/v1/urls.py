from django.urls import path

from apps.rentals.api.v1.views import initiate_rental_payment, create_checkout


urlpatterns=[
    path('create_checkout/', create_checkout),
    path('initiate_rental_payment/', initiate_rental_payment),
]