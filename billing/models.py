from django.db import models
from django.utils import timezone
from decimal import Decimal
from orders.models import Order

class Bill(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        CARD = 'CARD', 'Credit/Debit Card'
        UPI = 'UPI', 'UPI / QR Code'

    order = models.OneToOneField(Order, related_name='bill', on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_bill(self, tax_rate_percent: float = 5.0, discount_amount: Decimal = Decimal('0.00')):
        """Calculates tax, applies discount, and computes grand total."""
        subtotal = self.order.total_amount
        tax_val = (subtotal * Decimal(str(tax_rate_percent))) / Decimal('100.0')
        self.tax = tax_val.quantize(Decimal('0.01'))
        self.discount = Decimal(str(discount_amount)).quantize(Decimal('0.01'))
        
        computed_grand_total = subtotal + self.tax - self.discount
        self.grand_total = max(Decimal('0.00'), computed_grand_total).quantize(Decimal('0.01'))
        self.save()
        return self.grand_total

    def mark_as_paid(self, payment_method: str = 'CASH'):
        """Marks bill as paid, updates order status, and releases table."""
        self.payment_method = payment_method
        self.is_paid = True
        self.paid_at = timezone.now()
        self.save()

        # Update order status to COMPLETED
        self.order.status = Order.Status.COMPLETED
        self.order.save(update_fields=['status'])

        # Release table to AVAILABLE
        if self.order.table:
            self.order.table.mark_available()

        return self

    def __str__(self):
        status_text = "PAID" if self.is_paid else "UNPAID"
        return f"Bill for Order #{self.order.id} - ${self.grand_total} ({status_text})"
