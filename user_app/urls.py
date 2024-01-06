from django.urls import path
from user_app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('add/to/cart/<int:product_variant_id>/', add_to_cart, name='add-to-cart'),
    path('add/to/wishlist/<int:product_variant_id>/', add_to_wishlist, name='add-to-wishlist'),
    path('product/variant/details/<int:product_variant_id>/', product_variant_details, name='product-variant-details'),
    path('shop/', shop, name='shop'),
    path('cart/', cart, name='cart'),
    path('cart/<int:cart_id>/increase_quantity/', increase_quantity, name='increase-quantity'),
    path('cart/<int:cart_id>/decrease_quantity/', decrease_quantity, name='decrease-quantity'),
    path('cart/<int:cart_id>/delete/', delete_cart, name='delete-cart'),
    path('offer-product/', offer_product, name='offer-product'),
    path('category/<int:category_id>/', category_products, name='category-products'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<int:place_order_id>/', payment, name='payment'),
    path('payment/success/', payment_success, name='payment-success'),
    path('payment/field/', payment_field, name='payment-field'),
    
    
]