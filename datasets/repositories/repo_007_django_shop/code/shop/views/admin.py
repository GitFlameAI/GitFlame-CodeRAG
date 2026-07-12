from shop.models import Product
from shop.services.inventory import restock


def restock_product(catalog: dict[int, Product], product_id: int, qty: int) -> dict:
    product = catalog.get(product_id)
    if product is None:
        return {"status": 404, "error": "product not found"}
    if qty <= 0:
        return {"status": 400, "error": "qty must be positive"}
    restock(product, qty)
    return {"status": 200, "id": product.id, "stock": product.stock}
