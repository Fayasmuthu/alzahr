from decimal import Decimal

from django.conf import settings

CART_SESSION_KEY = getattr(settings, "CART_SESSION_KEY", "cart")
# COUPON_SESSION_KEY = getattr(settings, "COUPON_SESSION_KEY", "coupon")

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.coupon_id =settings.COUPON_ID
        cart = self.session.get(CART_SESSION_KEY)
        coupon =self.session.get(self.coupon_id)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

        if not coupon:
            coupon = self.session[self.coupon_id] = 0
        self.coupon = coupon

    def add(self, product_variant, quantity=1):
        product_id = str(product_variant.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "sale_price": str(product_variant.sale_price),
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product_variant):
        product_id = str(product_variant.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrease_quantity(self, product_variant):
        product_id = str(product_variant.id)
        if product_id in self.cart and self.cart[product_id]["quantity"] > 1:
            self.cart[product_id]["quantity"] -= 1
            self.save()

    def save(self):
        self.session.modified = True

    def get_cart(self):
        return self.cart.items()

    def get_total_price(self, item):
        return Decimal(item["quantity"]) * Decimal(item["sale_price"])

    def cart_total(self):
        c = Decimal(self.coupon)
        s =  sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in self.get_cart()
        )
        return s * c / 100

    def get_product_quantity(self, product_variant):
        product_id = str(product_variant.id)
        item = self.cart.get(product_id)
        if item:
            return item["quantity"]
        return 0

    def clear(self):
        del self.session[CART_SESSION_KEY]
        del self.session[self.coupon_id]
        self.save()

    def add_coupon(self, coupon_id):
        self.session[self.coupon_id] =coupon_id
        self.save()
        
    # def apply_discount(self, discount_percentage):
    #     for item_id, item_data in self.cart.items():
    #         sale_price = Decimal(item_data["sale_price"])
    #         item_data["sale_price"] = sale_price * (1 - discount_percentage / 100)
    #         # Update the cart item's total price
    #         item_data["total_price"] = item_data["quantity"] * item_data["sale_price"]

    # def remove_discount(self):
    #     for item_id, item_data in self.cart.items():
    #         # Reset the sale price to original
    #         original_price = Decimal(item_data["original_price"])
    #         item_data["sale_price"] = original_price
    #         # Update the cart item's total price
    #         item_data["total_price"] = item_data["quantity"] * item_data["sale_price"]

    def apply_discount(self, discount_percentage):
        for item_id, item_data in self.cart.items():
            sale_price = Decimal(item_data["sale_price"])
            item_data["sale_price"] = sale_price * (1 - discount_percentage / 100)
            item_data["total_price"] = item_data["quantity"] * item_data["sale_price"]

    def remove_discount(self):
        # Implement this method if needed
        pass