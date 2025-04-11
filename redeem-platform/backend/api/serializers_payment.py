from rest_framework import serializers
from .models import Transaction

class PaymentSerializer(serializers.Serializer):
    redeem_code_id = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=20)
    payment_details = serializers.JSONField()

class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'redeem_code', 'amount', 'status', 'payment_id', 'created_at']
