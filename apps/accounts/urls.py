from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.accounts.views import RegisterAPIView, NewTokenObtainPairView

urlpatterns = [
    path('', RegisterAPIView.as_view(), name='registration'),
    path('token/', NewTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]