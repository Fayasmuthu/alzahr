from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from orders.models import Wishlist
from product.models import Category, Producttype, Subcategory
import datetime

# from order.models import Wishlist


def main_context(request):
    categories = Category.objects.filter(status='Published')
    subcategory = Subcategory.objects.filter(active=True)
    product_type =Producttype.objects.all()
    wishlist_count = Wishlist.objects.filter(user=request.user.id).count()

    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    current_user = None
    name = ""

    if request.user.is_authenticated:
        if request.user.first_name and request.user.last_name:
            name = f"{request.user.first_name} {request.user.last_name}"
        else:
            name = request.user.username  # Fallback to username if first_name and last_name are not set

    current_user = request.user

    return {
        "categories": categories,
        "subcategories": subcategory,
        "product_type" :product_type,
        "domain": request.META["HTTP_HOST"],
        "current_version": "?v=2.0",
        "wishlist_count": wishlist_count,
        "default_user_avatar": f"https://ui-avatars.com/api/?name={name}&background=e8572e&color=fff&size=128",
        "greeting": greeting,
        "name": name,
        "current_user": current_user,
    }

