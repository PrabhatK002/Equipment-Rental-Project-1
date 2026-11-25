from django.urls import path

from apps.maintenances.api.v1.views import MaintenanceDetailView, MaintenanceView


urlpatterns=[
    path('', MaintenanceView.as_view()),
    path('<int:pk>/', MaintenanceDetailView.as_view()),
]