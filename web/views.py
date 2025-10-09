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
    template_name = "web/home/index.html"
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
        context["banner"] = Banner.objects.all()
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
    
class shopView(ListView):
    model = Product
    template_name = "web/shop.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True)
            # subcategories = Subcategory.objects.filter(active=True)
            sort_by = self.request.GET.get("sort_by")
            category_slugs = self.request.GET.get("categories")  # Updated query parameter for consistency
            subcategory_slugs = self.request.GET.get("subcategories")
            product_type_slugs = self.request.GET.get("product_type")
            category_title = None
            subcategory_title = None
            producttype_title = None


            # Filter by category
            if category_slugs:
                categories = Category.objects.filter(slug__in=category_slugs.split(","))
                subcategories = Subcategory.objects.filter(category__in=categories)
                producttypes = Producttype.objects.filter(Subcategory__in=subcategories)
                products = products.filter(product_type__in=producttypes)

            # Filter by Subcategory
            if subcategory_slugs:
                subcategories = Subcategory.objects.filter(slug__in=subcategory_slugs.split(","))
                producttypes = Producttype.objects.filter(Subcategory__in=subcategories)
                products = products.filter(product_type__in=producttypes)

            # Filter by Product Type
            if product_type_slugs:
                producttypes = Producttype.objects.filter(slug__in=product_type_slugs.split(","))
                # subcategories = Subcategory.objects.filter(producttype__in=producttypes)
                products = products.filter(product_type__in=producttypes)
            
                
            if sort_by:
                if sort_by == "low_to_high":
                    annotated_queryset = products.annotate(
                        min_sale_price_size=Min("available__sale_price"),
                        # min_sale_price_t=Min("available__sale_price")
                    )
                    products = annotated_queryset.order_by("min_sale_price_size")

                elif sort_by == "high_to_low":
                    annotated_queryset = products.annotate(
                        max_sale_price_size=Max("available__sale_price"),
                        # max_sale_price_t=Max("available__sale_price")
                    )
                    products = annotated_queryset.order_by("-max_sale_price_size")

                elif sort_by == "rating":
                    products = products.order_by("-rating")

                elif sort_by == "a_to_z":
                    products = products.order_by("title")

                elif sort_by == "z_to_a":
                    products = products.order_by("-title")

                else:
                    products = products.order_by("-id")

            self.category_title = category_title if category_title else None
            self.subcategory_title = subcategory_title if subcategory_title else None
            self.producttype_title = producttype_title if producttype_title else None

            return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.prefetch_related('subcategories').filter(status='Published')
        context["subcategories"] = Subcategory.objects.filter(active=True).prefetch_related('product_types')
        context["product_type"] = Producttype.objects.filter(active=True)
        context["title"] = self.category_title
        context["sub_title"] = self.subcategory_title
        return context


def coming_soon(request):
    context = {'is_contact': True} 
    return render(request, 'web/coming-soon.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product-image.html"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            current_product = self.get_object()
            product_ratings = [
                {"value": 5, "percentage": int(current_product.five_rating())},
                {"value": 4, "percentage": int(current_product.four_rating())},
                {"value": 3, "percentage": int(current_product.three_rating())},
                {"value": 2, "percentage": int(current_product.two_rating())},
                {"value": 1, "percentage": int(current_product.one_rating())},
            ]
            context["reviews"] = current_product.reviews.filter(approval=True)
            context["review_form"] = ReviewForm()
            context["product_ratings"] = product_ratings

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
