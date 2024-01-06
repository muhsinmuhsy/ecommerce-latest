from django.contrib import admin
from admin_app.models import *

# Register your models here.

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

@admin.register(ProductVariant)
class ProductVariantModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductVariant._meta.fields]

@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

@admin.register(BannerSlider)
class BannerSliderModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BannerSlider._meta.fields]

@admin.register(OfferBannerSlider)
class OfferBannerSliderModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OfferBannerSlider._meta.fields]

@admin.register(OfferProduct)
class OfferProductModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OfferProduct._meta.fields]

