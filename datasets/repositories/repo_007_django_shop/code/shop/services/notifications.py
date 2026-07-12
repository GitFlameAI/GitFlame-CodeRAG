from shop.models import Order


def order_confirmation_message(order: Order) -> dict:
    return {
        "to": f"order-{order.id}@customer",
        "subject": f"Order #{order.id} confirmed",
        "body": f"Your order #{order.id} with {len(order.items)} item(s) is now {order.status}.",
    }


def send(message: dict) -> bool:
    # Pretend to hand off to an email provider.
    return True
