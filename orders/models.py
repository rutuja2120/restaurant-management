from django.db import models
from decimal import Decimal
from tables.models import Table
from menu.models import MenuItem

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PREPARING = 'PREPARING', 'Preparing'
        SERVED = 'SERVED', 'Served'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    table = models.ForeignKey(Table, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_total(self):
        """Calculates total_amount by summing up subtotals of all OrderItems."""
        total = sum(order_item.get_subtotal() for order_item in self.items.all())
        self.total_amount = Decimal(str(total))
        self.save(update_fields=['total_amount'])
        return self.total_amount

    def add_item(self, item: MenuItem, quantity: int = 1):
        """Adds a MenuItem to the order. If already present, updates quantity."""
        if not item.is_available:
            raise ValueError(f"Menu item '{item.name}' is currently unavailable.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        order_item, created = OrderItem.objects.get_or_create(
            order=self,
            item=item,
            defaults={'price': item.price, 'quantity': quantity}
        )
        if not created:
            order_item.quantity += quantity
            order_item.save()

        # Update table status to OCCUPIED when an order is placed
        if self.table.status == Table.Status.AVAILABLE:
            self.table.mark_occupied()

        self.calculate_total()
        return order_item

    def advance_status(self):
        """Transitions order status to the next logical stage."""
        transitions = {
            self.Status.PENDING: self.Status.PREPARING,
            self.Status.PREPARING: self.Status.SERVED,
            self.Status.SERVED: self.Status.COMPLETED,
        }
        if self.status in transitions:
            self.status = transitions[self.status]
            self.save(update_fields=['status'])
        return self.status

    def __str__(self):
        return f"Order #{self.id} (Table {self.table.number}) - {self.get_status_display()} - ${self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.item.name} (${self.get_subtotal()})"
