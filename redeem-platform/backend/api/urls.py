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
from .views_payment import ProcessPaymentView, PaymentStatusView

router = DefaultRouter()
router.register(r'codes', RedeemCodeViewSet, basename='redeemcode')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/transaction-history/', TransactionViewSet.as_view({'get': 'transaction_history'}), name='transaction-history'),
    path('auth/update-profile/', UserProfileViewSet.as_view({'put': 'update_profile'}), name='update-profile'),
    path('payment/process/', ProcessPaymentView.as_view(), name='process-payment'),
    path('payment/status/<int:transaction_id>/', PaymentStatusView.as_view(), name='payment-status'),
]
