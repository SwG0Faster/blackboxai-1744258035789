from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import RedeemCode, Transaction, ActivityLog
from .serializers_payment import PaymentSerializer, PaymentResponseSerializer
import uuid

class ProcessPaymentView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            redeem_code_id = serializer.validated_data['redeem_code_id']
            payment_method = serializer.validated_data['payment_method']
            payment_details = serializer.validated_data['payment_details']

            # Get the redeem code
            redeem_code = get_object_or_404(RedeemCode, id=redeem_code_id)

            # Verify code is available
            if redeem_code.buyer or not redeem_code.is_active:
                return Response(
                    {"error": "Code is not available for purchase"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Process payment (mock implementation)
                payment_id = str(uuid.uuid4())  # Generate unique payment ID
                
                # Create transaction
                transaction = Transaction.objects.create(
                    redeem_code=redeem_code,
                    buyer=request.user,
                    seller=redeem_code.seller,
                    amount=redeem_code.selling_price,
                    status='COMPLETED',
                    payment_id=payment_id
                )

                # Update redeem code status
                redeem_code.buyer = request.user
                redeem_code.is_active = False
                redeem_code.save()

                # Log activity
                ActivityLog.objects.create(
                    user=request.user,
                    action=f"Purchased code {redeem_code.code} for ₹{redeem_code.selling_price} via {payment_method}"
                )

                # Return transaction details
                response_serializer = PaymentResponseSerializer(transaction)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Log the error and return error response
                ActivityLog.objects.create(
                    user=request.user,
                    action=f"Payment failed for code {redeem_code.code}: {str(e)}"
                )
                return Response(
                    {"error": "Payment processing failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentStatusView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id, buyer=request.user)
        serializer = PaymentResponseSerializer(transaction)
        return Response(serializer.data)
