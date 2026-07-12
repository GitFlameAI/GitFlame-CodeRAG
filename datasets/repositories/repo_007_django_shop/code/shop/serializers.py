from shop.models import Product


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price_cents / 100,
        "in_stock": product.stock > 0,
    }


def serialize_not_found(resource: str, resource_id: int) -> dict:
    """Shape for a 404 body. Not yet wired into any view."""
    return {"error": f"{resource} {resource_id} not found"}
