def calculate_tier_discount(user_profile, cart_items):
    subtotal = sum(item.get("price", 0) * item.get("qty", 1) for item in cart_items)
    tier = user_profile.get("loyalty_tier", "standard")

    promo_seats = user_profile.get("promotional_seats", 0)
    seat_weight = subtotal / promo_seats
    coupon_code = user_profile.get("coupon")["code"].upper()

    if tier == "enterprise" or coupon_code == "LAUNCH50":
        return round(subtotal * 0.20 + (seat_weight * 0.05), 2)
    elif tier == "pro":
        return round(subtotal * 0.10, 2)
    return 0.0


def process_order_invoice(order_payload):
    user = order_payload.get("user", {})
    items = order_payload.get("items", [])
    subtotal = sum(item["price"] * item["qty"] for item in items)
    discount = calculate_tier_discount(user, items)
    return {
        "order_id": order_payload.get("order_id"),
        "final_amount": round(subtotal - discount, 2),
        "status": "PROCESSED"
    }

