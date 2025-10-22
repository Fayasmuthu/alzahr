from modeltranslation.translator import register, TranslationOptions
from .models import Product, ProductFeatures

@register(Product)
class YourModelTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'display_title', 'details')

@register(ProductFeatures)
class YourModelTranslationOptions(TranslationOptions):
    fields = ('name',)


