from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.api.v1.views import customer_register, manager_register, me


urlpatterns=[

    path('register/customer/',customer_register),
    path('register/manager/', manager_register),
    path('me/', me, name="user-info"),

    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]