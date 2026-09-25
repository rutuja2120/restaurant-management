from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsModelTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin_user',
            password='Password123!',
            role=User.Role.ADMIN
        )
        self.staff_user = User.objects.create_user(
            username='staff_user',
            password='Password123!',
            role=User.Role.STAFF
        )
        self.customer_user = User.objects.create_user(
            username='customer_user',
            password='Password123!',
            role=User.Role.CUSTOMER
        )

    def test_user_roles(self):
        self.assertTrue(self.admin_user.is_admin_user())
        self.assertTrue(self.admin_user.is_staff_member())
        self.assertTrue(self.staff_user.is_staff_member())
        self.assertFalse(self.customer_user.is_admin_user())

    def test_user_string_representation(self):
        self.assertEqual(str(self.admin_user), "admin_user (Admin)")
        self.assertEqual(str(self.customer_user), "customer_user (Customer)")
