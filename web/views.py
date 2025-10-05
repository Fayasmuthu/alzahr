import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Min, Max
from collections import defaultdict
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
import urllib.parse
from web.models import Contactmessage
from web.forms import ContactForm
from orders.models import Wishlist
from orders.forms import WhatsAppOrderForm
from product.forms import ReviewForm
from product.models import Banner, Brand, Category,Product,Producttype,Subcategory
from django.db.models import Q


class indexView(TemplateView):
    template_name = "web/index-2.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(status='Published')
        context["subcategories"] = Subcategory.objects.filter(active=True)
        context["product_type"] = Producttype.objects.all()
        products = Product.objects.filter(is_active=True)
        context["brands"] = Brand.objects.all()
        context["new_arrvied"] = products.filter(is_arrive=True)
        context["popular_products"] = products.filter(is_popular=True)
        context["best_seller_products"] = products.filter(is_best_seller=True)
        wishlist_count = Wishlist.objects.filter(user=self.request.user.id).count()
        context["wishlist_count"] = wishlist_count
        context["products"] = Product.objects.all()
        # context["recent_products"] = products.order_by('-created_at')[:10]
        context["recent_products"] = products.order_by('-id')[:10]
        
        category_title = self.request.GET.get("category")
        if category_title:
                # category_title = Category.objects.get(slug=category_title)
                category_title = get_object_or_404(Category, slug=category_title)
                # category_title = get_object_or_404(Category, slug=category_title)
                products = products.filter(product_type__Subcategory__category=category_title)
                # Check for subcategory and filter products accordingly
                context["products"] = products

        subcategory = self.request.GET.get("subcategory")
        if subcategory:
            subcategory_title = get_object_or_404(Subcategory, slug=subcategory)
            products = products.filter(product_type__Subcategory__category=subcategory_title)               
            context["products"] = products     
        return context
    
    # In your product detail view
    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        viewed = request.session.get('recently_viewed', [])
        if product.id not in viewed:
            viewed.insert(0, product.id)
            request.session['recently_viewed'] = viewed[:10]  # Keep only last 10
        return render(request, "product/detail.html", {"product": product})
  
    
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