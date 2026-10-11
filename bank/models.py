from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

class Customer(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    cust_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=16, unique=True, blank=True)
    address = models.TextField(max_length=200)
    dob = models.DateField(null=True, blank=True)
    mob_no = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.account_no:
            # Unique constraint remains the final safeguard against collisions.
            import secrets
            while True:
                candidate = "PY" + "".join(str(secrets.randbelow(10)) for _ in range(10))
                if not Customer.objects.filter(account_no=candidate).exists():
                    self.account_no = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cust_name} ({self.account_no})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdrawal"),
        ("TRANSFER", "Transfer"),
    ]
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    from_customer = models.ForeignKey(
        Customer, related_name="outgoing_transactions",
        null=True, blank=True, on_delete=models.PROTECT
    )
    to_customer = models.ForeignKey(
        Customer, related_name="incoming_transactions",
        null=True, blank=True, on_delete=models.PROTECT
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount} ({self.pk})"
