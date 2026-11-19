"""Demonstration CLI for the inventory system."""
from inventory import Inventory, Product, PerishableProduct


def main() -> None:
    inventory = Inventory()
    inventory.add_product(Product("P001", "Notebook", 20, reorder_level=5))
    inventory.add_product(PerishableProduct(
        "P002", "Milk", 4, "2027-01-15", reorder_level=5
    ))

    inventory.products["P001"].remove_stock(3)
    inventory.products["P002"].add_stock(2)

    print(inventory.generate_report())
    print("\n=== LOW STOCK ALERTS ===")
    alerts = inventory.get_low_stock_alerts()
    if alerts:
        for product in alerts:
            print(product)
    else:
        print("No low-stock products.")


if __name__ == "__main__":
    main()
