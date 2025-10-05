from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from django.urls import reverse_lazy
from tinymce.models import HTMLField
from django.utils import timezone


from main.choices import ICON_CHOICES, STATUS_CHOICES, UNIT_CHOICES

# Create your models here.

class Banner(models.Model):
    title =models.CharField(max_length=100)
    content = models.CharField(max_length=100,default=False)
    image=models.ImageField(upload_to="banner/img")
    other1 = models.BooleanField(default=False)
    other2 = models.BooleanField(default=False)
    other3 = models.BooleanField(default=False)
    other4 = models.BooleanField(default=False)
    other5 = models.BooleanField(default=False)
    other6 = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banner")
        ordering = ("image",)

class Brand(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image=models.ImageField(upload_to="brand/img", null=True, blank=True)
    active = models.BooleanField(default=True)
    filter_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class Color(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    color = models.CharField(max_length=7, null=True, blank=True, help_text="Hex color, e.g., #FF5733")

    def __str__(self):
        return str(self.title)

class Category(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to="categories/img",  default=False)
    icon_image =models.ImageField(upload_to="categories/icon", default=False)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES,default="Published")
    active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Category1= models.BooleanField(default=False)
    Category2= models.BooleanField(default=False)
    Category3= models.BooleanField(default=False)
    Category4= models.BooleanField(default=False)
    Category5= models.BooleanField(default=False)
    Category6= models.BooleanField(default=False)
    Category7= models.BooleanField(default=False)

    class Meta:
            verbose_name = _("Category")
            verbose_name_plural = _("Categories")
            ordering = ("title",)

    
    def __str__(self):
        return str(self.title)

class Subcategory(models.Model):
    category =models.ForeignKey("product.Category", on_delete=models.CASCADE,related_name="subcategories")
    title= models.CharField(max_length=100)
    slug = models.SlugField()
    image=models.ImageField(null=True, blank=True, upload_to="subcategories/img",  default=False)
    icon_image =models.ImageField(upload_to="subcategories/icon",  default=False)
    color = models.CharField(max_length=7, null=True, blank=True, help_text="Hex color, e.g., #FF5733")
    active=models.BooleanField(default=True,null=True,blank=True)
    is_combo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")
        ordering = ("title",)

    def get_sub_products(self):
        return Producttype.objects.filter(subcategory=self)

    def get_absolute_url(self):
        return reverse_lazy("web:shop", kwargs={"slug": self.slug})
    
    def get_sub_product_count(self):
        return self.get_sub_products().count()
    
    def __str__(self):
        return f"{self.category}--{self.title}" if self.category else self.title

class Producttype(models.Model):
    Subcategory =models.ForeignKey("product.Subcategory", on_delete=models.CASCADE,related_name="product_types")
    title= models.CharField(max_length=100)
    slug = models.SlugField()
    active=models.BooleanField(default=True,null=True,blank=True)
    is_combo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product type")
        verbose_name_plural = _("Product type")
        ordering = ("title",)

    def get_sub_products(self):
        return Product.objects.filter(product_type=self)

    def get_sub_product_count(self):
        return self.get_sub_products().count()
    
    def __str__(self):
        return f"{self.Subcategory}--{self.title}" if self.Subcategory else self.title

class Product(models.Model):
    product_type = models.ForeignKey(
        "product.Producttype", on_delete=models.CASCADE, related_name="Producttype"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    display_title = models.CharField(max_length=200, null=True, blank=True)
    stock=models.IntegerField(null=False,default="1")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, default="Generic")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    details = HTMLField(null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    model_number = models.CharField(max_length=200,null=True, blank=True)
    rating = models.FloatField(
        validators=[MaxValueValidator(5.0)],
        default=5.0,
        verbose_name="Product Rating (max: 5)"
    )
    image = models.ImageField(
        upload_to="products/img", help_text=" The recommended size is 700x955 pixels."
    )
    # created_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_arrive = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # meta
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=500, blank=True, null=True)
    other1 = models.BooleanField(default=False)
    other2 = models.BooleanField(default=False)
    other3 = models.BooleanField(default=False)
    other4 = models.BooleanField(default=False)
    other5 = models.BooleanField(default=False)
    section1 = models.BooleanField(default=False)
    section2 = models.BooleanField(default=False)
    section3 = models.BooleanField(default=False)
    section4 = models.BooleanField(default=False)
    section5 = models.BooleanField(default=False)
    section6 = models.BooleanField(default=False)
    section7 = models.BooleanField(default=False)
    section8 = models.BooleanField(default=False)
    section9 = models.BooleanField(default=False)
    section10 = models.BooleanField(default=False)
    
    class Meta:
        ordering = [ "id",]
        verbose_name = "Product"
        verbose_name_plural = "Products"


    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_image(self):
        return ProductImage.objects.filter(product=self).first()

    def get_sizes(self):
        return AvailableSize.objects.filter(product=self)

    def get_sale_price(self):
        sizes = self.get_sizes()
        if sizes.exists():  # Check if queryset is not empty
            return min([p.sale_price for p in sizes])
        return None  # Return a default value when sizes are empty

    def get_regular_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.regular_price for p in sizes if p.regular_price is not None]
        if valid_prices:  # Check if the list of valid prices is not empty
            return min(valid_prices)
        return None  #

    def get_offer_percent_first(self):
        first_size = self.get_sizes().first()
        if first_size and hasattr(first_size, 'offer_percent') and callable(getattr(first_size, 'offer_percent')):
            return first_size.offer_percent()
        return None

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_sizes()])

    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]

    def get_absolute_url(self):
        return reverse_lazy("web:product_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse_lazy("main:product_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:product_delete", kwargs={"pk": self.pk})
    
    def get_sizes_t(self):
        return Available.objects.filter(product=self)
    
    def get_infrom(self):
        return ProductInformation.objects.filter(product=self)
    
    def get_features(self):
        return ProductFeatures.objects.filter(product=self)

    def get_sale_price_t(self):
        sizes = self.get_sizes_t()
        if sizes.exists():  # Check if queryset is not empty
            return min([p.sale_price for p in sizes])
        return None  # Return a default value when sizes are empty

    def get_regular_price_t(self):
        sizes = self.get_sizes_t()
        valid_prices = [p.regular_price for p in sizes if p.regular_price is not None]
        if valid_prices:  # Check if the list of valid prices is not empty
            return min(valid_prices)
        return None

    def get_offer_percent_first_t(self):
        first_size = self.get_sizes_t().first()
        if first_size and hasattr(first_size, 'offer_percent_t') and callable(getattr(first_size, 'offer_percent_t')):
            return first_size.offer_percent_t()
        return None  # Or any default value or action you prefer if there's no offer_percent_t


    def get_offer_percent(self):
        sizes = self.get_sizes_t()
        valid_percentages = [p.offer_percent_t() for p in sizes if hasattr(p, 'offer_percent_t') and callable(getattr(p, 'offer_percent_t'))]
        if valid_percentages:  # Check if the list of valid percentages is not empty
            return min(valid_percentages)
        return None

    def get_first_varient(self):
        return AvailableSize.objects.filter(product=self).first()


    def get_reviews(self):
        return Review.objects.filter(product=self, approval=True)

    def num_of_reviews(self):
        return self.get_reviews().count()

    def average_rating(self):
        from django.db.models import Avg

        return self.get_reviews().aggregate(Avg("rating"))["rating__avg"]

    def five_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=5).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=5).count()
            else 0
        )

    def four_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=4).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=4).count()
            else 0
        )

    def three_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=3).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=3).count()
            else 0
        )

    def two_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=2).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=2).count()
            else 0
        )

    def one_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=1).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=1).count()
            else 0
        )
    
    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(review.rating for review in reviews) / reviews.count()
        else:
            self.rating = 0
        self.save()

    def __str__(self):
        return self.title

class ProductInformation(models.Model):
    product = models.ForeignKey(
        "Product", verbose_name="Product Information", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f" {self.product}"
    
class ProductFeatures(models.Model):
    product = models.ForeignKey(
        "Product", verbose_name="Product Information", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f" {self.product}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/img-detail", help_text=" The recommended size is 800x600 pixels."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("product",)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)


class AvailableSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES,blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    regular_price  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Available Size")
        verbose_name_plural = _("Available Sizes")
        ordering = ("sale_price",)

    def offer_percent(self):
        if self.regular_price and self.regular_price != self.sale_price:
            return ((self.regular_price - self.sale_price) / self.regular_price) * 100
        return 0

    def save(self, *args, **kwargs):
        if self.regular_price is None:
            self.regular_price = self.sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.unit} "


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Customer Rating (1 to 5)"
    )
    fullname = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval = models.BooleanField(default=True)

    def __str__(self):  
        return f"{self.headline} - {self.product.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()
   
class Available(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    regular_price  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_stock = models.BooleanField(default=True)
 
    class Meta:
        verbose_name = _("Available ")
        verbose_name_plural = _("Available")
        ordering = ("sale_price",)
    
    def offer_percent_t(self):
        if self.regular_price is not None and self.sale_price is not None:
            if self.regular_price != self.sale_price:
                return ((self.regular_price - self.sale_price) / self.regular_price) * 100
        return 0


    def save(self, *args, **kwargs):
        if self.regular_price is None:
            self.regular_price = self.sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product}"
    
