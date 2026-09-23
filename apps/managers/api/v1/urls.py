from django.urls import path
from apps.managers.api.v1.views import ManagerView, ManagerDetailView


urlpatterns = [
    path('', ManagerView.as_view()),
    path('<int:pk>/', ManagerDetailView.as_view())
]