from modeltranslation.translator import register, TranslationOptions
from .models import Product

@register(Product)
class YourModelTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'details')


