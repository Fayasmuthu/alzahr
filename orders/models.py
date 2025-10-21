import uuid
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.db import models

from product.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Available", on_delete=models.CASCADE)

    class Meta:
        # unique_together = ("user", "product")
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")

    def __str__(self):
        return f"{self.product.product.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"{self.title}"

def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]
    return f"{timestamp}{unique_id.upper()}"

class Order(models.Model):
    unique_transaction_id = models.UUIDField(
        unique=True, editable=False, blank=True, null=True
    )
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=255, default=generate_order_id)
    is_ordered = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=(("COD", "Cash On Delivery"), ("OP", "Online Payment")),
        default="COD",
    )

    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField("Complete Address", max_length=100)
    address_line_2 = models.CharField("Landmark", max_length=100)
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100)
    pin_code = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    alternative_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Placed", "Order Placed"),
            ("Shipped", "Order Shipped"),
            ("InTransit", "In Transit"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )
    payment_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Success", "Success"),
            ("Cancelled", "Cancelled"),
        ),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-id",)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_products(self):
        return Product.objects.filter(order=self)

    def get_grand_total(self):
        total = self.payable + self.service_fee + self.shipping_fee
        return total

    def order_total(self):
        return float(sum([item.subtotal for item in self.get_items()]))

    def get_user_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"order_id": self.order_id})

    def __str__(self):
        return f"{self.order_id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Available", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    image =models.ImageField()


    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.order} - {self.product}"

    def subtotal(self):
        return self.price * self.quantity


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,choices=(("COD","Cash On Delivery"),("OP","Online Payment")),default="COD")
    payment_id = models.CharField(max_length=50,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.order_id}"

class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount = models.PositiveBigIntegerField(help_text="discount in percentage")
    active =models.BooleanField(default=True)
    active_date =models.DateField()
    expiry_date =models.DateField()
    created_date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    

class WhatsAppOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="whatsapp_orders")
    quantity = models.PositiveIntegerField(default=1)
    selected_size = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order for {self.product.title} ({self.selected_size}) x {self.quantity}"
    class Meta:
        # unique_together = ("user", "product")
        verbose_name = _("Whatsapp order")
        verbose_name_plural = _("Whatsapp Order")