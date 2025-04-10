from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RedeemCodeViewSet,
    TransactionViewSet,
    UserProfileViewSet,
    RegistrationView,
    LoginView,
    LogoutView
)

router = DefaultRouter()
router.register(r'codes', RedeemCodeViewSet, basename='redeemcode')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
