from django.contrib import admin
from django.utils.safestring import mark_safe
from web.models import Contactmessage
from product.models import Available, AvailableSize, Banner, Brand, Category, Color, Product, ProductFeatures, ProductImage, ProductInformation, Producttype, Review, Subcategory

# Register your models here.
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}    

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}  
    
admin.site.register(Contactmessage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "status")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status",)
    search_fields = ("title",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.icon_image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class AvailableInline(admin.TabularInline):
    model = Available
    extra = 1

class ProductInformationInline(admin.TabularInline):
    model = ProductInformation
    extra = 1


class ProductFeaturesInline(admin.TabularInline):
    model = ProductFeatures
    extra = 1

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title','image_preview', 'slug')
    prepopulated_fields = {"slug": ("title",)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"

def save(self, *args, **kwargs):
    if not self.image:
        self.image = None  
    super().save(*args, **kwargs)

@admin.register(Producttype)
class ProducttypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'Subcategory','active')
    prepopulated_fields = {"slug": ("title",)}

class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", 'is_active')
    exclude = ("creator",)
    list_filter = (   
        "is_best_seller",
        "is_offer",
        "is_active",
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "producttype__title", "producttype__subcategory__title")
    inlines = [
        ProductImageInline,AvailableInline, ProductInformationInline,ProductFeaturesInline,
        AvailableSizeInline
        ]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"

class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "weight",
        "unit",
        "sale_price",
        "regular_price",
        "is_stock",
    )
    list_filter = ("product", "unit", "is_stock")


admin.site.register(Review)
