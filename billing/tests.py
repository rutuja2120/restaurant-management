from django.test import TestCase
from decimal import Decimal
from tables.models import Table
from menu.models import Category, MenuItem
from orders.models import Order
from billing.models import Bill

class BillingTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=2, capacity=2, status=Table.Status.OCCUPIED)
        self.category = Category.objects.create(name='Beverages')
        self.coffee = MenuItem.objects.create(
            category=self.category,
            name='Espresso',
            price=Decimal('5.00'),
            is_available=True
        )

        self.order = Order.objects.create(table=self.table)
        self.order.add_item(self.coffee, quantity=4) # Total = 4 * 5.00 = $20.00

    def test_bill_calculation(self):
        bill = Bill.objects.create(order=self.order)
        # Calculate with 10% tax and $2.00 discount
        # Tax = $20.00 * 0.10 = $2.00
        # Grand Total = $20.00 + $2.00 - $2.00 = $20.00
        grand_total = bill.calculate_bill(tax_rate_percent=10.0, discount_amount=Decimal('2.00'))

        self.assertEqual(bill.tax, Decimal('2.00'))
        self.assertEqual(bill.discount, Decimal('2.00'))
        self.assertEqual(bill.grand_total, Decimal('20.00'))
        self.assertFalse(bill.is_paid)

    def test_payment_processing(self):
        bill = Bill.objects.create(order=self.order)
        bill.calculate_bill(tax_rate_percent=5.0, discount_amount=Decimal('0.00'))
        
        # Mark as paid via UPI
        bill.mark_as_paid(payment_method=Bill.PaymentMethod.UPI)

        self.assertTrue(bill.is_paid)
        self.assertEqual(bill.payment_method, Bill.PaymentMethod.UPI)

        # Check that order is marked COMPLETED
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.COMPLETED)

        # Check that table is automatically freed to AVAILABLE
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, Table.Status.AVAILABLE)
