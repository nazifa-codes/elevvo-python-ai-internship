"""Object-oriented inventory management with perishable-product expiry checks."""
from datetime import date


class Product:
    """A general product with validated stock and a low-stock threshold."""

    def __init__(self, product_id: str, name: str, stock: int,
                 reorder_level: int = 5) -> None:
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.reorder_level = reorder_level

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Stock must be a non-negative integer.")
        self._stock = value

    def add_stock(self, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to add must be a positive integer.")
        self.stock += quantity

    def remove_stock(self, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to remove must be a positive integer.")
        if quantity > self.stock:
            raise ValueError("Insufficient stock.")
        self.stock -= quantity

    def is_low_stock(self) -> bool:
        return self.stock <= self.reorder_level

    def report_line(self) -> str:
        status = "LOW STOCK" if self.is_low_stock() else "In stock"
        return (f"{self.product_id} | {self.name} | "
                f"Stock: {self.stock} | {status}")

    def __str__(self) -> str:
        return self.report_line()


class PerishableProduct(Product):
    """A product that also tracks expiry and can report expired status."""

    def __init__(self, product_id: str, name: str, stock: int,
                 expiry_date: str, reorder_level: int = 5) -> None:
        super().__init__(product_id, name, stock, reorder_level)
        try:
            self.expiry_date = date.fromisoformat(expiry_date)
        except ValueError as exc:
            raise ValueError("Expiry date must use YYYY-MM-DD.") from exc

    def is_expired(self, on_date: date | None = None) -> bool:
        """Return True when expiry date is earlier than the check date."""
        check_date = on_date or date.today()
        return self.expiry_date < check_date

    def report_line(self) -> str:
        status = "EXPIRED" if self.is_expired() else "Not expired"
        stock_status = "LOW STOCK" if self.is_low_stock() else "In stock"
        return (f"{self.product_id} | {self.name} | Stock: {self.stock} | "
                f"{stock_status} | Expiry: {self.expiry_date.isoformat()} "
                f"({status})")


class Inventory:
    """Manage products and produce a formatted inventory report."""

    def __init__(self) -> None:
        self.products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if product.product_id in self.products:
            raise ValueError(f"Product ID already exists: {product.product_id}")
        self.products[product.product_id] = product

    def get_low_stock_alerts(self) -> list[Product]:
        return [product for product in self.products.values()
                if product.is_low_stock()]

    def generate_report(self) -> str:
        lines = ["=== INVENTORY REPORT ==="]
        if not self.products:
            lines.append("No products in inventory.")
        else:
            lines.extend(product.report_line()
                         for product in self.products.values())
        lines.append(f"Total product types: {len(self.products)}")
        return "\n".join(lines)
