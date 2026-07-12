class PaymentFailed(Exception):
    """Raised when the payment gateway declines or errors on a charge."""

    def __init__(self, order_id: int, reason: str):
        self.order_id = order_id
        self.reason = reason
        super().__init__(f"payment failed for order {order_id}: {reason}")


class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"product {product_id} not found")
