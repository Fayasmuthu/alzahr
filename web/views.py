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
from product.models import Available, AvailableSize, Banner, Brand, Category,Product,Producttype,Subcategory
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import urllib
from orders.models import WhatsAppOrder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        context["dried"] = Product.objects.filter(dried=True)
        context["powder"] = Product.objects.filter(powder=True)
        context["whole"] = Product.objects.filter(whole=True)
        context["Slice"] = Product.objects.filter(Slice=True)
        context["top"] = Product.objects.filter(top=True)
        context["incense"] = Product.objects.filter(incense=True)
        context["health"] = Product.objects.filter(health=True)
        context["non_salt"] = Product.objects.filter(non_salt=True)
        context["seeds"] = Product.objects.filter(seeds=True)
        context["section5"] = Product.objects.filter(section5=True)
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
                review = form.save(commit=False)
                review.product = product
                review.user = user
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
                    "message": str(form.errors),
                }
        else:
            response_data = {
                "status": "false",
                "title": "User not authenticated",
                "message": "User must be authenticated to submit a review.",
            }

        return JsonResponse(response_data)


# ✅ ADD THIS NEW VIEW FOR WHATSAPP ORDERS
@require_POST
def save_whatsapp_order(request):
    try:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        variant_type = request.POST.get('variant_type')
        variant_id = request.POST.get('variant_id')

        # Validate required fields
        if not all([product_id, quantity, variant_type, variant_id]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)

        # Get the product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Product not found'
            }, status=404)

        # Save the order (adjust based on your model structure)
        # Example:
        whatsapp_order = WhatsAppOrder.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product=product,
            quantity=quantity,
            variant_type=variant_type,
            variant_id=variant_id,
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Order saved successfully',
            'order_id': whatsapp_order.id
        })

    except Exception as e:
        print(f"Error saving WhatsApp order: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to save order'
        }, status=500)


def coming_soon(request):
    context = {'is_contact': True} 
    return render(request, 'web/coming-soon.html', context)


@csrf_exempt
def save_whatsapp_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        variant_type = request.POST.get('variant_type')
        variant_id = request.POST.get('variant_id')

        product = get_object_or_404(Product, id=product_id)
        variant_label = None

        if variant_type == 'size':
            size_obj = get_object_or_404(AvailableSize, id=variant_id)
            variant_label = f"{size_obj.weight}{size_obj.unit}"
        elif variant_type == 'available':
            available_obj = get_object_or_404(Available, id=variant_id)
            variant_label = f"Price AED {available_obj.sale_price}"

        WhatsAppOrder.objects.create(
            product=product,
            quantity=int(quantity),
            selected_size=variant_label
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@require_POST
@csrf_exempt
def update_order_status(request):
    order_id = request.POST.get('order_id')
    status = request.POST.get('status')
    order = get_object_or_404(WhatsAppOrder, id=order_id)
    order.status = status
    order.save()
    return JsonResponse({'success': True})

def search_view(request):
    query = request.GET.get('q', '').strip()
    categories = subcategories = producttypes = products = None

    if query:
        # Search Categories
        categories = Category.objects.filter(
            Q(title__icontains=query) | Q(slug__icontains=query)
        )

        # Search Subcategories
        subcategories = Subcategory.objects.filter(
            Q(title__icontains=query) | Q(slug__icontains=query)
        )

        # Search Product Types
        producttypes = Producttype.objects.filter(
            Q(title__icontains=query) | Q(slug__icontains=query)
        )

        # Search Products
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(slug__icontains=query) | Q(brand__title__icontains=query)
        )

    context = {
        'query': query,
        'categories': categories,
        'subcategories': subcategories,
        'producttypes': producttypes,
        'products': products,
    }
    return render(request, 'web/search_results.html', context)

def cn(request):
    products = Product.objects.all()
    categories = Category.objects.filter(status='Published')
    subcategory = Subcategory.objects.filter(active=True)
    
    context = {
        'is_contact': True,
        'products': products,
        'categories': categories,
        'subcategories': subcategory,
        } 
    
    category_title = request.GET.get("category")
    if category_title:
            # category_title = Category.objects.get(slug=category_title)
            category_title = get_object_or_404(Category, slug=category_title)
            # category_title = get_object_or_404(Category, slug=category_title)
            products = products.filter(product_type__Subcategory__category=category_title)
            context['products'] = products
            
    subcategory = request.GET.get("subcategory")
    if subcategory:
        subcategory_title = get_object_or_404(Subcategory, slug=subcategory)
        products = products.filter(product_type__Subcategory__category=subcategory_title)               
        context["products"] = products     
   
    return render(request, 'web/cn.html', context)



class driedView(ListView):
    model = Product
    template_name = "web/shop/dried.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, dried=True)
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
        wishlist_count = Wishlist.objects.filter(user=self.request.user.id).count()
        context["wishlist_count"] = wishlist_count
        return context
    
class powderView(ListView):
    model = Product
    template_name = "web/shop/powder.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, powder=True)
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
    
class incenseView(ListView):
    model = Product
    template_name = "web/shop/Incense.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, incense=True)
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
    
class wholeView(ListView):
    model = Product
    template_name = "web/shop/whole.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, whole=True)
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
    
class topView(ListView):
    model = Product
    template_name = "web/shop/top.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, top=True)
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
    
class sliceView(ListView):
    model = Product
    template_name = "web/shop/slice.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, slice=True)
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
    
class seedView(ListView):
    model = Product
    template_name = "web/shop/seed.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, seed=True)
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
    
class nonsaltView(ListView):
    model = Product
    template_name = "web/shop/non-salt.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, non_salt=True)
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
    
class healthView(ListView):
    model = Product
    template_name = "web/shop/health.html"
    context_object_name = "products"
    paginate_by = 16

    def get_queryset(self):
            products = Product.objects.filter(is_active=True, health=True)
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