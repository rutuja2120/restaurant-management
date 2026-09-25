from django.test import TestCase
from decimal import Decimal
from menu.models import Category, MenuItem

class MenuModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Main Course', description='Delicious main dishes')
        self.item = MenuItem.objects.create(
            category=self.category,
            name='Margherita Pizza',
            price=Decimal('12.50'),
            is_available=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Main Course')
        self.assertEqual(str(self.category), 'Main Course')

    def test_menu_item_creation(self):
        self.assertEqual(self.item.name, 'Margherita Pizza')
        self.assertEqual(self.item.price, Decimal('12.50'))
        self.assertTrue(self.item.is_available)
        self.assertEqual(str(self.item), 'Margherita Pizza - $12.50 (Available)')
