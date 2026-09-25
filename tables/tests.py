from django.test import TestCase
from tables.models import Table

class TableModelTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, capacity=4, status=Table.Status.AVAILABLE)

    def test_table_creation(self):
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertTrue(self.table.is_available())

    def test_table_status_transitions(self):
        self.table.mark_occupied()
        self.assertEqual(self.table.status, Table.Status.OCCUPIED)
        self.assertFalse(self.table.is_available())

        self.table.mark_reserved()
        self.assertEqual(self.table.status, Table.Status.RESERVED)

        self.table.mark_available()
        self.assertEqual(self.table.status, Table.Status.AVAILABLE)
        self.assertTrue(self.table.is_available())
