from django.urls import path

from apps.equipments.api.v1.views import CategoryDetailView, CategoryView, EquipmentDetailView, EquipmentView

urlpatterns=[
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    path('', EquipmentView.as_view()),
    path('<int:pk>/', EquipmentDetailView.as_view())
]