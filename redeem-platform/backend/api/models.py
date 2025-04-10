from django.db import models
from django.contrib.auth.models import User

class RedeemCode(models.Model):
    PLATFORM_CHOICES = [
        ('PAYTM', 'Paytm'),
        ('PHONEPE', 'PhonePe'),
        ('GOOGLEPAY', 'Google Pay'),
        ('AMAZONPAY', 'Amazon Pay'),
    ]
    
    CODE_TYPE_CHOICES = [
        ('CASHBACK', 'Cashback'),
        ('DISCOUNT', 'Discount'),
        ('REWARD', 'Reward Points'),
        ('VOUCHER', 'Gift Voucher'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes_selling')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='codes_bought')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICES)
    code_value = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=100)
    expiry_date = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform} {self.code_type} - ₹{self.code_value}"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    redeem_code = models.ForeignKey(RedeemCode, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_as_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_as_seller')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_sales = models.IntegerField(default=0)
    total_purchases = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
