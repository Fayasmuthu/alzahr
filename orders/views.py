from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
# from main.models import District
from product.forms import ReviewForm
from orders.forms import OrderForm
from orders.models import Coupon, Order, OrderItem, Wishlist
from orders.cart import Cart
from django.contrib import messages
from product.models import Available, AvailableSize, Product
# import razorpay

import urllib.parse

from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

# import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
# Create your views here.


# CART
def cart_view(request):
    cart = Cart(request)
    cart_items = []


    for item_id, item_data in cart.get_cart():
        variant = get_object_or_404(AvailableSize, id=item_id)
        quantity = item_data["quantity"]
        total_price = Decimal(item_data["sale_price"]) * quantity
        cart_items.append(
            {
                "product": variant,
                "quantity": quantity,
                "total_price": total_price,

            }
        )
    context = {
        "cart_items": cart_items,
        "cart_total": sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in cart.get_cart()
        ),

    }
    return render(request, "web/cart.html", context)


def cart_add(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User not authenticated'}, status=401)
    cart = Cart(request)
    cart_instance = cart.cart
    quantity = request.GET.get("quantity", 1)
    product_id = request.GET.get("product_id", "")
    variant = get_object_or_404(AvailableSize, pk=product_id)
    cart.add(variant, quantity=int(quantity))
    return JsonResponse(
        {
            "message": "Product Quantity Added from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[product_id]),
            "cart_total": cart.cart_total(),
            "cart_count": len(cart_instance),
        }
    )


def clear_cart_item(request, item_id):
    cart = Cart(request)
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.remove(variant)
    return redirect(reverse("orders:cart"))


def minus_to_cart(request):
    cart = Cart(request)
    cart_instance = cart.cart
    item_id = request.GET.get("item_id")
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.decrease_quantity(variant)
    return JsonResponse(
        {
            "message": "Product Quantity decreased from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[item_id]),
            "cart_total": cart.cart_total(),
        }
    )


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("web:shop"))

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.get_object()
            user = request.user
            form = ReviewForm(request.POST, request.FILES)

            if form.is_valid():
                review = form.save(commit=False)  # Use commit=False to create a Review instance but not save it yet
                review.product = product
                review.user = user  # Set the user for the review
                review.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Message successfully Submitted",
                }
                # if form.is_valid():
                #     form.instance.product = product
                #     form.save()
                #     response_data = {
                #         "status": "true",
                #         "title": "Successfully Submitted",
                #         "message": "Message successfully Submitted",
                #     }
            else:
                print(form.errors)
                response_data = {
                    "status": "false",
                    "title": "Form validation error",
                    "message": form.errors,
                }
        else:
            response_data = {
                "status": "false",
                "title": "User not authenticated",
                "message": "User must be authenticated to submit a review.",
            }

        return JsonResponse(response_data)


class AddToWishlistView(View):
    def get(self, request ):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Available, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            wishlist_count = Wishlist.objects.filter(user=request.user.id).count()
            return JsonResponse({'message': 'Product Added from Wishlist successfullyy',
                                 'wishlist_count': wishlist_count})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.'})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        return JsonResponse({'message': 'Product Removed from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})


class AddCoupon (View):
    def get(self, *args, **kwargs):
        code =self.request.GET.get('coupon')
        coupon =Coupon.objects.filter(code__iexact=code)
        cart = Cart(self.request)
        if coupon.exists():
            coupon = coupon.first()
            current_date = datetime.date(timezone.now())
            active_date = coupon.active_date
            expiry_date = coupon.expiry_date

            if current_date > expiry_date:
                return JsonResponse({
                    "message": "The coupon Expired",
                    'alert':'alert-warning'
                })

            elif current_date < active_date:
                return JsonResponse({
                    "message": "The coupon is yet to be available",
                    'alert':'alert-danger'
                })
            else:
                cart = Cart(self.request)
                cart.add_coupon(coupon.discount)
                return JsonResponse({
                        "message": "The coupon has been included successfully !",
                        'alert':'alert-success',
                        'amt':coupon.discount,
                        'discount': coupon.discount,
                        'total':cart.cart_total()

                    })
        else:
            return JsonResponse(
                {
                    "message": "Invalid coupon code",
                    'alert':'alert-danger',
                })


def order(request):
    if request.method == "POST":
        cart = Cart(request)
        products = ""
        total = 0
        counter = 1
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(Available, id=item_id)
            quantity = item_data["quantity"]
            price = Decimal(item_data["sale_price"])
            if variant.product.subcategory.is_combo:
                products += f"{counter}.{variant.product.name} ({quantity}x{price}) ₹ {variant.weight*quantity} \n ----------------------- \n"
            else:
                products += f"{counter}.{variant.product.name}-{variant.weight} {variant.unit} ({quantity}x{price}) ₹ {variant.sale_price*quantity} \n ----------------------- \n"
            total += quantity * variant.sale_price
            counter += 1

        message = (
            f"============================\n"
            f"Welcome to BLUE TOWER.\n"
            f"============================\n\n"
            f'Name: {request.POST.get("name")}\n'
            f'Phone: {request.POST.get("phone")}\n'
            f'Address: {request.POST.get("address")}\n'
            f"----------------------------\n\n"
            f"Products:\n"
            f"{products}\n\n"
            f"Grand Total: {total}\n"
            f"============================\n"
            f"Final bill will be based on the product availability and amount derived there upon.\n\n"
            f"Thank you for shopping with us.\n "
        )

        whatsapp_api_url = "https://api.whatsapp.com/send"
        phone_number = "+971503495411"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"
        cart.clear()
        return redirect(whatsapp_url)



class CheckoutView(View):
    template_name = "web/checkout.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        form = OrderForm()
        context = {
            "cart_items": cart_items,
            "cart_total": sum(item["total_price"] for item in cart_items),
            "form": form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = Cart(request)
        if cart is not None:
            cart_items = self.get_cart_items(cart)
            # Continue processing cart_items
        else:
            # Handle the case where cart is None
            # You might want to set cart_items to an empty list or handle it differently
            cart_items = []
        if form.is_valid():
            selected_dial_code_mobile = form.cleaned_data.get(
                "selected_dial_code_mobile"
            )
            selected_dial_code_alternative = form.cleaned_data.get(
                "selected_dial_code_alternative"
            )
            m_n = form.cleaned_data.get("mobile_no")
            a_n = form.cleaned_data.get("alternative_no")
            mobile_no = f"{selected_dial_code_mobile}{m_n}"
            alternative_no = f"{selected_dial_code_alternative}{a_n}"

            data = form.save(commit=False)
            data.subtotal = request.POST.get("payable")
            data.service_fee = request.POST.get("service_fee")
            data.shipping_fee = request.POST.get("shipping_fee")
            data.payable = request.POST.get("total_amt")
            data.payment_method = request.POST.get("selected_payment")
            data.mobile_no = mobile_no
            data.alternative_no = alternative_no
            data.save()
            for item_id, item_data in cart.get_cart():
                variant = get_object_or_404(AvailableSize, id=item_id)
                quantity = item_data["quantity"]
                price = Decimal(item_data["sale_price"])
                # product = Product.objects.get(id=item_id)
                # image = str(product.image)

                order_item = OrderItem.objects.create(
                    order=data,
                    product=variant,
                    price=price,
                    quantity=quantity,
                    # image = image,
                )

                # Handle image upload for the order item
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    # Ensure the uploaded file is an image
                    if image_file.content_type.startswith('image'):
                        order_item.image = image_file
                        order_item.save()
                    else:
                        # Handle invalid image file
                        order_item.delete()
                        raise ValidationError("Invalid image file format.")

                order_item.save()
            if data.payment_method == "OP":
                return redirect("orders:payment", pk=data.pk)
            else:
                return redirect("orders:complete_order", pk=data.pk)
        else:
            context = {
                "cart_items": cart_items,
                "cart_total": sum(item["total_price"] for item in cart_items),
                "form": form,
            }
            return render(request, self.template_name, context)

    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "total_price": total_price,

                }
            )
        return cart_items

from django.conf import settings

@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()

            products = ""
            total = 0
            counter = 1
            for item in order.get_items():
                if item.product.product.subcategory.is_combo:
                    products += f"{counter}.{item.product.product.name} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
                else:
                    products += f"{counter}.{item.product.product.name}- {item.product.unit} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
                total += item.subtotal()
                counter += 1

            message = (
                f"============================\n"
                f"Order Confirmed\n"
                f"============================\n\n"
                f"Order ID: {order.order_id}\n"
                f"Order Date: {order.created}\n"
                f"Order Status: Placed\n"
                f"Payment Method: Online Payment\n"
                f"Payment Status: Success\n"
                f"----------------------------\n\n"
                f"Products:\n\n"
                f"{products}\n\n"
                f"----------------------------\n\n"
                f"Order Summary:\n\n"
                f"Subtotal: {order.subtotal} \n"
                f"service fee: {order.service_fee} \n"
                f"shipping fee: {order.shipping_fee} \n\n"
                f"Total Payble: {order.payable} \n\n"
                f"----------------------------\n\n"
                f"Shipping Address:\n\n"
                f"Name: {order.full_name}\n"
                f"Address: {order.address_line_1}\n"
                f"Landmark: {order.address_line_2}\n"
                f"State: {order.state}\n"
                f"District: {order.district}\n"
                f"City: {order.city}\n"
                f"Pincode: {order.pin_code}\n"
                f"Mobile: {order.mobile_no}\n"
                f"Email: {order.email}\n\n"
                f"Thank you for placing your order with Blue Tower. Your order has been confirmed.\n\n"
            )

            email = order.email
            subject = "Order Confirmation - Blue Tower"
            message = message
            send_mail(
                subject,
                message,
                "fayas@gmail.com",
                [email,"fayas@gmail.com"],
                fail_silently=False,
            )

            print("email sent successfully")
            cart = Cart(request)
            cart.clear()

        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("orders:payment", pk=order.pk)


class CompleteOrderView(DetailView):
    model = Order
    template_name = "web/order-success.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_ordered = True
        order.order_status = "Placed"
        order.save()
        products = ""
        total = 0
        counter = 1
        for item in order.get_items():
            if item.product.product.subcategory.is_combo:
                products += f"{counter}.{item.product.product.name} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
            else:
                products += f"{counter}.{item.product.product.name}- {item.product.unit} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
            total += item.subtotal()
            counter += 1

        message = (
            f"============================\n"
            f"Order Confirmed\n"
            f"============================\n\n"
            f"Order ID: {order.order_id}\n"
            f"Order Date: {order.created}\n"
            f"Order Status: Placed\n"
            f"Payment Method: Cash On Delivery\n"
            f"Payment Status: Pending\n"
            f"----------------------------\n"
            f"Products:\n\n"
            f"{products}\n"
            f"----------------------------\n"
            f"Order Summary:\n\n"
            f"Subtotal: {order.subtotal} \n"
            f"service fee: {order.service_fee} \n"
            f"shipping fee: {order.shipping_fee} \n\n"
            f"Total Payble: {order.payable} \n\n"
            f"----------------------------\n"
            f"Shipping Address:\n\n"
            f"Name: {order.full_name}\n"
            f"Address: {order.address_line_1}\n"
            f"Landmark: {order.address_line_2}\n"
            f"State: {order.state}\n"
            f"District: {order.district}\n"
            f"City: {order.city}\n"
            f"Pincode: {order.pin_code}\n"
            f"Mobile: {order.mobile_no}\n"
            f"Email: {order.email}\n\n"
            f"Thank you for placing your order with Blue Tower. Your order has been confirmed.\n\n"
        )

        email = order.email
        subject = "Order Confirmation - Blue Tower"
        message = message
        send_mail(
            subject,
            message,
            "fayasmuthu45@gmail.com",
            [email,"fayasmuthu45@gmail.com"],
            fail_silently=False,
        )

        cart = Cart(request)
        cart.clear()
        context = {
            "object": order,
        }
        return render(request, self.template_name, context)


class UserOrderDetailView(DetailView):
    model = Order
    template_name = "web/invoice/invoice-1.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"my_order": True}


