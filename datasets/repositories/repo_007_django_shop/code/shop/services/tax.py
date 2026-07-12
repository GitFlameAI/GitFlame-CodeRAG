DEFAULT_TAX_RATE = 0.0825


def calculate_tax(subtotal_cents: int, rate: float = DEFAULT_TAX_RATE) -> int:
    return round(subtotal_cents * rate)
