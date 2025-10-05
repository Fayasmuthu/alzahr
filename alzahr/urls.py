from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("web.urls", namespace="web")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("product.urls", namespace="product")),
    path("", include("orders.urls", namespace="orders")),
    # path("", include("shop.urls", namespace="shop")),
]
