from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import RedeemCode, Transaction, UserProfile
from .serializers import (
    RedeemCodeSerializer, 
    TransactionSerializer, 
    UserProfileSerializer,
    UserRegistrationSerializer,
    LoginSerializer
)

@method_decorator(csrf_exempt, name='dispatch')
class RedeemCodeViewSet(viewsets.ModelViewSet):
    queryset = RedeemCode.objects.all()
    serializer_class = RedeemCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter codes based on query parameters"""
        queryset = RedeemCode.objects.filter(is_active=True)
        platform = self.request.query_params.get('platform', None)
        code_type = self.request.query_params.get('code_type', None)
        min_value = self.request.query_params.get('min_value', None)
        max_value = self.request.query_params.get('max_value', None)

        if platform:
            queryset = queryset.filter(platform=platform)
        if code_type:
            queryset = queryset.filter(code_type=code_type)
        if min_value:
            queryset = queryset.filter(code_value__gte=min_value)
        if max_value:
            queryset = queryset.filter(code_value__lte=max_value)

        return queryset

    @action(detail=False, methods=['get'])
    def transaction_history(self, request):
        """Retrieve transaction history for the authenticated user"""
        transactions = Transaction.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
        return Response(TransactionSerializer(transactions, many=True).data)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update user profile information"""
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        code = self.get_object()
        if code.buyer or not code.is_active:
            return Response(
                {"error": "Code is not available for purchase"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create activity log
        ActivityLog.objects.create(
            user=request.user,
            action=f"Purchased code: {code.code} for ₹{code.selling_price}"
        )

        # Create transaction
        transaction = Transaction.objects.create(
            redeem_code=code,
            buyer=request.user,
            seller=code.seller,
            amount=code.selling_price,
            status='PENDING'
        )

        # Update code status
        code.buyer = request.user
        code.is_active = False
        code.save()

        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_201_CREATED
        )

@method_decorator(csrf_exempt, name='dispatch')
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Show transactions where user is either buyer or seller"""
        return Transaction.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        )

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        profile = self.get_queryset().first()
        if profile:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        return Response({"detail": "Profile not found"}, status=404)

class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserProfileSerializer(user.userprofile).data,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authtoken.models import Token

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "user": UserProfileSerializer(user.userprofile).data,
                    "token": token.key,
                    "message": "Login successful"
                })
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"})
