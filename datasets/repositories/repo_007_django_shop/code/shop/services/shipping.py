FLAT_RATE_CENTS = 500
FREE_SHIPPING_THRESHOLD_CENTS = 5000


def shipping_cost(subtotal_cents: int) -> int:
    if subtotal_cents >= FREE_SHIPPING_THRESHOLD_CENTS:
        return 0
    return FLAT_RATE_CENTS
