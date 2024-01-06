from django.db import models
from auth_app.models import User 
from admin_app.models import Product, ProductVariant
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Place_Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField()

class Order_Item(models.Model):
    ORDER_STATUS = (
        ('PENDING', 'PENDING'),
        ('CARTED', 'CARTED'),
        ('PAID', 'PAID'),
    )
    DELIVERY_STATUS = (
        ('PENDING', 'PENDING'),
        ('ORDER CORNFIMED', 'ORDER CORNFIMED'),
        ('SHIPPED', 'SHIPPED'),
        ('ORDER DON', 'ORDER DON'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    place_order = models.ForeignKey(Place_Order, on_delete=models.CASCADE, null=True, blank=True)

    # price always change thats why this using
    actual_price_dummy = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price_dummy = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    quantity = models.IntegerField(default=1)

    
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default='PENDING', null=True, blank=True)
    delivery_status = models.CharField(max_length=100, choices=DELIVERY_STATUS, default='PENDING', null=True, blank=True)

# # automatically saving price dummy from product price 
# @receiver(pre_save, sender=Order_Item)
# def auto_save_price_dummy(sender, instance, **kwargs):
#     product_variant = instance.product_variant
#     # if there is discount price saving siscount price else saving actual price
#     if product_variant:
#         if product_variant.discount_price:
#             instance.price_dummy = product_variant.discount_price
#         else:
#             instance.price_dummy = product_variant.actual_price

# # atomatically calculating the price_dummy*quantity
# @receiver(pre_save, sender=Order_Item)
# def auto_cart_total(sender, instance, **kwargs):
#     instance.total = instance.price_dummy * instance.quantity   



class Payment(models.Model):
    PAYMENT_STATUS = (
        ('TRIED' ,'TRIDE'),
        ('SUCCESS', 'SUCCESS'),
        ('FIELD', 'FIELD')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    order_item = models.ManyToManyField(Order_Item)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='TRIED', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)