from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = (
    [
    path('admin/', admin.site.urls),
    path("", include("web.urls", namespace="web")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("product.urls", namespace="product")),
    path("", include("orders.urls", namespace="orders")),
    # path("", include("shop.urls", namespace="shop")),

    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    # path('djrichtextfield/', include('djrichtextfield.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('registration.backends.simple.urls')),

]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "Blue Tower Group Administration"
admin.site.site_title = "Blue Tower Group Admin Portal"
admin.site.index_title = "Welcome to Blue Tower Group Admin Portal"
