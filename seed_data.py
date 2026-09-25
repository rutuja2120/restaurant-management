import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tables.models import Table
from menu.models import Category, MenuItem
from orders.models import Order
from billing.models import Bill

User = get_user_model()

def seed_database():
    print("Seeding Restaurant Management System Database...")

    # 1. Create Superuser / Staff Users
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@restaurant.com',
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("  [+] Created Admin User: admin / admin123")

    staff_user, created = User.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'staff@restaurant.com',
            'role': User.Role.STAFF,
            'is_staff': True
        }
    )
    if created:
        staff_user.set_password('staff123')
        staff_user.save()
        print("  [+] Created Staff User: staff / staff123")

    # 2. Create Restaurant Tables
    tables_data = [
        (1, 2, Table.Status.AVAILABLE),
        (2, 2, Table.Status.AVAILABLE),
        (3, 4, Table.Status.OCCUPIED),
        (4, 4, Table.Status.AVAILABLE),
        (5, 6, Table.Status.RESERVED),
        (6, 8, Table.Status.AVAILABLE),
    ]
    for num, cap, st in tables_data:
        t, _ = Table.objects.get_or_create(number=num, defaults={'capacity': cap, 'status': st})
        print(f"  [+] Table #{t.number} ({t.capacity} seats) -> {t.status}")

    # 3. Create Categories & Menu Items
    cat_starters, _ = Category.objects.get_or_create(name='Appetizers', defaults={'description': 'Fresh starters & finger food'})
    cat_mains, _ = Category.objects.get_or_create(name='Main Course', defaults={'description': 'Hearty main dishes & pizzas'})
    cat_drinks, _ = Category.objects.get_or_create(name='Beverages', defaults={'description': 'Refreshing cold & hot drinks'})
    cat_desserts, _ = Category.objects.get_or_create(name='Desserts', defaults={'description': 'Sweet artisanal treats'})

    items_data = [
        (cat_starters, 'Garlic Bread sticks', 6.50, 'Toasted with herb garlic butter'),
        (cat_starters, 'Crispy Chicken Wings', 9.99, 'Spicy buffalo glaze with ranch'),
        (cat_mains, 'Margherita Pizza', 14.50, 'Fresh mozzarella, basil & tomato sauce'),
        (cat_mains, 'Grilled Salmon Steak', 22.00, 'Served with asparagus & lemon butter'),
        (cat_mains, 'Classic Cheeseburger', 12.50, 'Angus beef patty with cheddar cheese'),
        (cat_drinks, 'Iced Lemon Tea', 3.50, 'Freshly brewed iced tea'),
        (cat_drinks, 'Espresso Coffee', 4.00, 'Double shot dark roast espresso'),
        (cat_desserts, 'Chocolate Lava Cake', 7.50, 'Warm molten chocolate cake with vanilla ice cream'),
    ]

    for cat, name, price, desc in items_data:
        m, _ = MenuItem.objects.get_or_create(name=name, defaults={'category': cat, 'price': price, 'description': desc, 'is_available': True})
        print(f"  [+] Menu Item: {m.name} - ${m.price}")

    # 4. Create Sample Active Order on Table 3
    table3 = Table.objects.get(number=3)
    order, created = Order.objects.get_or_create(table=table3, status=Order.Status.PREPARING)
    if created:
        pizza = MenuItem.objects.get(name='Margherita Pizza')
        wings = MenuItem.objects.get(name='Crispy Chicken Wings')
        tea = MenuItem.objects.get(name='Iced Lemon Tea')

        order.add_item(pizza, 1)
        order.add_item(wings, 2)
        order.add_item(tea, 2)
        print(f"  [+] Sample Active Order #{order.id} for Table 3 Total: ${order.total_amount}")

        # Create Bill for Order
        bill, _ = Bill.objects.get_or_create(order=order)
        bill.calculate_bill(tax_rate_percent=5.0, discount_amount=2.00)
        print(f"  [+] Generated Bill for Order #{order.id}: Grand Total = ${bill.grand_total}")

    print("Database Seeding Completed Successfully!")

if __name__ == '__main__':
    seed_database()
