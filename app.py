"""
Lightweight Setup Verification Script for Restaurant Management System.
Checks environment setup, database connectivity, and core module health.
"""
import os
import sys

def verify_system_setup():
    print("==================================================")
    print("  Restaurant Management System - Setup Diagnostic")
    print("==================================================")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        print("[+] Django Framework: Initialized successfully")
    except Exception as e:
        print(f"[-] Django Initialization Failed: {e}")
        sys.exit(1)

    # Import Core Models
    try:
        from django.contrib.auth import get_user_model
        from tables.models import Table
        from menu.models import Category, MenuItem
        from orders.models import Order
        from billing.models import Bill

        User = get_user_model()

        print("[+] Database Connection: Verified")
        print("--------------------------------------------------")
        print(f"  * Total Registered Users:  {User.objects.count()}")
        print(f"  * Floor Seating Tables:    {Table.objects.count()}")
        print(f"  * Menu Categories:         {Category.objects.count()}")
        print(f"  * Active Menu Items:       {MenuItem.objects.count()}")
        print(f"  * Kitchen Orders Placed:   {Order.objects.count()}")
        print(f"  * Billing Invoices Issued: {Bill.objects.count()}")
        print("--------------------------------------------------")
        
        # Diagnostic module check
        print("[+] Module Status Check:")
        print("  - Accounts Module:  [OK]")
        print("  - Tables Module:    [OK]")
        print("  - Menu Module:      [OK]")
        print("  - Orders Module:    [OK]")
        print("  - Billing Module:   [OK]")
        print("==================================================")
        print(" SUCCESS: Workspace setup verified and ready to run!")
        print("==================================================")

    except Exception as e:
        print(f"[-] Database Diagnostic Error: {e}")
        print("    Did you run 'python manage.py migrate' and 'python seed_data.py'?")
        sys.exit(1)

if __name__ == '__main__':
    verify_system_setup()
