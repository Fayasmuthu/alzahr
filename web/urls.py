from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", views.indexView.as_view(), name="index"),
    path("shop/", views.shopView.as_view(), name="shop"),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path("product-detail/<slug:slug>/",views.ProductDetailView.as_view(),name="product_detail"),
    path('search/', views.search_view, name='search'),
    path('order/<slug:product_slug>/whatsapp/', views.order_via_whatsapp, name='order_via_whatsapp'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('cn/', views.cn, name='cn'),

    # ------shop---------
    path("dried/", views.driedView.as_view(), name="dried"),
    path("powder/", views.powderView.as_view(), name="powder"),
    path("incense/", views.incenseView.as_view(), name="incense"),
    path("whole/", views.wholeView.as_view(), name="whole"),
    path("top/", views.topView.as_view(), name="top"),
    path("slice/", views.sliceView.as_view(), name="slice"),
    path("seed/", views.seedView.as_view(), name="seed"),
    path("non-salt/", views.nonsaltView.as_view(), name="non_salt"),
    path("health/", views.healthView.as_view(), name="health"),



]