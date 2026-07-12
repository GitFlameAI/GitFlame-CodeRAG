from shop.models import Order


class InvalidCoupon(Exception):
    pass


# code -> percent off, e.g. 10 means 10% off
COUPONS: dict[str, int] = {
    "WELCOME10": 10,
    "SAVE20": 20,
}


def apply_discount(subtotal_cents: int, coupon_code: str | None) -> int:
    if not coupon_code:
        return subtotal_cents
    percent = COUPONS.get(coupon_code)
    if percent is None:
        raise InvalidCoupon(coupon_code)
    return subtotal_cents - (subtotal_cents * percent // 100)


def order_total_with_discount(order: Order, catalog: dict, coupon_code: str | None = None) -> int:
    from shop.models import order_total

    subtotal = order_total(order, catalog)
    return apply_discount(subtotal, coupon_code)
