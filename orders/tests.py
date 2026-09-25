from django.test import TestCase
from decimal import Decimal
from tables.models import Table
from menu.models import Category, MenuItem
from orders.models import Order, OrderItem

class OrderLogicTestCase(TestCase):
    def setUp(self):
        # Create Table
        self.table = Table.objects.create(number=5, capacity=4, status=Table.Status.AVAILABLE)

        # Create Category & Menu Items
        self.category = Category.objects.create(name='Fast Food')
        self.burger = MenuItem.objects.create(
            category=self.category,
            name='Cheeseburger',
            price=Decimal('10.50'),
            is_available=True
        )
        self.fries = MenuItem.objects.create(
            category=self.category,
            name='French Fries',
            price=Decimal('4.00'),
            is_available=True
        )
        self.soda = MenuItem.objects.create(
            category=self.category,
            name='Cold Soda',
            price=Decimal('2.50'),
            is_available=True
        )
        self.unavailable_item = MenuItem.objects.create(
            category=self.category,
            name='Special Cake',
            price=Decimal('15.00'),
            is_available=False
        )

        # Create Order
        self.order = Order.objects.create(table=self.table)

    def test_order_initialization(self):
        """Test initial order state."""
        self.assertEqual(self.order.table, self.table)
        self.assertEqual(self.order.status, Order.Status.PENDING)
        self.assertEqual(self.order.total_amount, Decimal('0.00'))

    def test_item_addition_and_total_bill_calculation(self):
        """Test adding items to order and recalculating total bill amount."""
        # Add 2 Burgers ($10.50 * 2 = $21.00)
        self.order.add_item(self.burger, quantity=2)
        self.assertEqual(self.order.total_amount, Decimal('21.00'))

        # Add 3 Sodas ($2.50 * 3 = $7.50) -> Total $28.50
        self.order.add_item(self.soda, quantity=3)
        self.assertEqual(self.order.total_amount, Decimal('28.50'))

        # Add 1 Fries ($4.00 * 1 = $4.00) -> Total $32.50
        self.order.add_item(self.fries, quantity=1)
        self.assertEqual(self.order.total_amount, Decimal('32.50'))

        # Check OrderItem count
        self.assertEqual(self.order.items.count(), 3)

    def test_add_existing_item_increments_quantity(self):
        """Test that adding an existing item increments its quantity and updates total."""
        self.order.add_item(self.burger, quantity=1)
        self.assertEqual(self.order.total_amount, Decimal('10.50'))

        # Add 2 more burgers
        self.order.add_item(self.burger, quantity=2)
        self.assertEqual(self.order.total_amount, Decimal('31.50')) # 3 * 10.50

        order_item = OrderItem.objects.get(order=self.order, item=self.burger)
        self.assertEqual(order_item.quantity, 3)

    def test_table_marked_occupied_on_order(self):
        """Test table status automatically changes from AVAILABLE to OCCUPIED when order item added."""
        self.assertEqual(self.table.status, Table.Status.AVAILABLE)
        self.order.add_item(self.burger, quantity=1)
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, Table.Status.OCCUPIED)

    def test_add_unavailable_item_raises_error(self):
        """Test adding an out-of-stock item raises a ValueError."""
        with self.assertRaises(ValueError):
            self.order.add_item(self.unavailable_item, quantity=1)

    def test_invalid_quantity_raises_error(self):
        """Test adding zero or negative quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.order.add_item(self.burger, quantity=0)

        with self.assertRaises(ValueError):
            self.order.add_item(self.burger, quantity=-2)

    def test_order_status_advancement(self):
        """Test order status workflow: PENDING -> PREPARING -> SERVED -> COMPLETED."""
        self.assertEqual(self.order.status, Order.Status.PENDING)

        self.order.advance_status()
        self.assertEqual(self.order.status, Order.Status.PREPARING)

        self.order.advance_status()
        self.assertEqual(self.order.status, Order.Status.SERVED)

        self.order.advance_status()
        self.assertEqual(self.order.status, Order.Status.COMPLETED)
