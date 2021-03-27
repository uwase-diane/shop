from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import(
    OrderSummary,
    CheckoutView,
    )


urlpatterns=[
    path('',views.index,name = 'index'),
    path('shop/',views.products,name = 'products'),
    path('category/<category>',views.product_category,name = 'category'),
    path('product/<id>', views.product_details, name='product'),
    path('product/', views.add_review, name='product'),
    path('shippingpolicy/',views.shippingpolicy, name='shippingpolicy'),
    path('order_summary/', OrderSummary.as_view(), name="order_summary"),
    path('accounts/profile/', views.my_profile, name="profile"),
    path('add-to-cart/<id>', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<id>', views.remove_from_cart, name="remove-from-cart"),
    path('remove-single-item/<id>', views.remove_single_item, name="remove-single-item"),
    path('search/', views.search_item, name="search"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('subscribe/', views.subscribe, name="subscribe"),
    
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)