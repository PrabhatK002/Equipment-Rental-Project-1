from django.urls import path

from apps.locations.api.v1.views import LocationDetailView, LocationView

urlpatterns = [
    path('',LocationView.as_view()),
    path('<int:pk>/', LocationDetailView.as_view())
]