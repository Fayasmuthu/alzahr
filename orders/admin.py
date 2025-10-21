from django.contrib import admin
from .models import WhatsAppOrder
from django.utils.html import format_html
# Register your models here.

@admin.register(WhatsAppOrder)
class WhatsAppOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'selected_size', 'quantity', 'customer_name', 'customer_phone', 'colored_status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('product__title', 'customer_name', 'customer_phone')
    ordering = ('-order_date',)

    fieldsets = (
        ('Order Information', {
            'fields': ('product', 'selected_size', 'quantity', 'status')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('order_date',),
        }),
    )

    readonly_fields = ('order_date',)  # ✅ to prevent changing order date manually

    def colored_status(self, obj):
        from django.utils.html import format_html
        color_map = {
            'pending': '#ffc107',    # yellow
            'shipping': '#17a2b8',   # blue
            'delivered': '#28a745',  # green
            'cancelled': '#dc3545',  # red
        }
        color = color_map.get(obj.status, '#000')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())
    colored_status.short_description = "Status"
