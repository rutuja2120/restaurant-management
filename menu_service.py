"""
Menu Service Utility - Restaurant Management System
Provides functions for case-insensitive menu search and price filtering.
"""

SAMPLE_MENU = [
    {
        'id': 1,
        'name': 'Garlic Breadsticks',
        'category': 'Appetizers',
        'price': 6.50,
        'is_available': True
    },
    {
        'id': 2,
        'name': 'Crispy Chicken Wings',
        'category': 'Appetizers',
        'price': 9.99,
        'is_available': True
    },
    {
        'id': 3,
        'name': 'Margherita Pizza',
        'category': 'Main Course',
        'price': 14.50,
        'is_available': True
    },
    {
        'id': 4,
        'name': 'Classic Cheeseburger',
        'category': 'Main Course',
        'price': 12.50,
        'is_available': True
    },
    {
        'id': 5,
        'name': 'Grilled Salmon Steak',
        'category': 'Main Course',
        'price': 22.00,
        'is_available': True
    },
    {
        'id': 6,
        'name': 'Iced Lemon Tea',
        'category': 'Beverages',
        'price': 3.50,
        'is_available': True
    },
    {
        'id': 7,
        'name': 'Espresso Coffee',
        'category': 'Beverages',
        'price': 4.00,
        'is_available': True
    },
    {
        'id': 8,
        'name': 'Chocolate Lava Cake',
        'category': 'Desserts',
        'price': 7.50,
        'is_available': True
    }
]


def search_menu(query: str, items: list = None) -> list:
    """
    Performs case-insensitive filtering by item name or category.
    Returns a list of matching menu items.
    """
    if items is None:
        items = SAMPLE_MENU

    if not query:
        return list(items)

    query_lower = str(query).lower().strip()
    results = [
        item for item in items
        if query_lower in item['name'].lower() or query_lower in item['category'].lower()
    ]
    return results


def filter_by_price(max_price: float, items: list = None) -> list:
    """
    Returns items whose price is less than or equal to max_price.
    """
    if items is None:
        items = SAMPLE_MENU

    max_p = float(max_price)
    return [item for item in items if item['price'] <= max_p]


if __name__ == '__main__':
    print("Testing Menu Service Search & Filter Functions...")

    # Test 1: Case-insensitive search by item name
    pizza_results = search_menu('pizza')
    assert len(pizza_results) == 1
    assert pizza_results[0]['name'] == 'Margherita Pizza'
    print("  [+] Test 1 Passed: search_menu('pizza')")

    # Test 2: Case-insensitive search by category
    beverage_results = search_menu('beverages')
    assert len(beverage_results) == 2
    assert all(item['category'] == 'Beverages' for item in beverage_results)
    print("  [+] Test 2 Passed: search_menu('beverages')")

    # Test 3: Price filtering <= 10.0
    budget_results = filter_by_price(10.0)
    assert len(budget_results) == 5 # Garlic Bread, Wings, Tea, Coffee, Cake
    assert all(item['price'] <= 10.0 for item in budget_results)
    print("  [+] Test 3 Passed: filter_by_price(10.0)")

    # Test 4: Combined search and price filtering
    appetizer_under_8 = filter_by_price(8.0, search_menu('appetizers'))
    assert len(appetizer_under_8) == 1
    assert appetizer_under_8[0]['name'] == 'Garlic Breadsticks'
    print("  [+] Test 4 Passed: Combined search & price filter")

    print("\nSUCCESS: All menu_service.py assertions passed successfully!")
