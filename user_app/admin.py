from django.contrib import admin
from user_app.models import *

# Register your models here.
@admin.register(Place_Order)
class Place_OrderModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Place_Order._meta.fields]

@admin.register(Order_Item)
class Order_ItemModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order_Item._meta.fields]

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wishlist._meta.fields]