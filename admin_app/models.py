from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='category-images')
    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    image_two = models.ImageField(upload_to='product_images', null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    product_details = models.CharField(max_length=1000, null=True, blank=True)
    hide = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    offer_percentage = models.FloatField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    hide = models.BooleanField(default=False)
    
@receiver(pre_save, sender=ProductVariant)
def calculate_offer_percentage(sender, instance, **kwargs):
    # Calculate offer percentage based on actual price and discount price
    if instance.actual_price is not None and instance.discount_price is not None:
        if instance.actual_price != 0:  # Avoid division by zero
            instance.offer_percentage = ((instance.actual_price - instance.discount_price) / instance.actual_price) * 100
        else:
            # Handle the case when actual price is zero
            instance.offer_percentage = 0
    else:
        # If actual price or discount price is not provided, set offer percentage to None
        instance.offer_percentage = None

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class BannerSlider(models.Model):
    image = models.ImageField(upload_to='banner-slider', null=True, blank=True)

class OfferBannerSlider(models.Model):
    image = models.ImageField(upload_to='offer-banner-slider', null=True, blank=True)

class OfferProduct(models.Model):
    product = models.ManyToManyField(Product)