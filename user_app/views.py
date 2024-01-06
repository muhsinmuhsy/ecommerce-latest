from django.shortcuts import render, redirect
from admin_app.models import Product, ProductVariant, Category, BannerSlider, OfferBannerSlider, OfferProduct, ProductImage
from user_app.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import JsonResponse

# Create your views here.

def home(request):
    current_page = 'home'
    catagories = Category.objects.all()
    banner_sliders = BannerSlider.objects.all()
    offer_banner_sliders = OfferBannerSlider.objects.all()
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        product_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_variant', flat=True)
    else:
        product_wishlist = None


    context = {
        'current_page': current_page,
        'categories' : catagories,
        'products' : products,
        'banner_sliders' : banner_sliders,
        'offer_banner_sliders' : offer_banner_sliders,
        'product_wishlist' : product_wishlist
    }
    return render(request, 'user/pages/home.html', context)


def add_to_cart(request, product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    product = product_variant.product
    user = request.user

    cart, created = Order_Item.objects.get_or_create(
        user=user,
        product_variant=product_variant,
        order_status='CARTED'
    )

    # If the order-item item already exists, increment the quantity
    if not created:
        cart.quantity += 1
        cart.save()
    messages.success(request, f"{product.name, product_variant.name}, Added to cart successfully")
    # Redirect the user to the previous page (history)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_to_wishlist(request, product_variant_id):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    product = product_variant.product

    # Check if the product is already in the user's wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product_variant=product_variant)

    if created:
        messages.success(request, f"{product.name, product_variant.name} added to wishlist successfully")
    else:
        wishlist_item.delete()
        messages.success(request, f"{product.name, product_variant.name} removed from wishlist successfully")

    
    # Redirect the user to the previous page (history)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



# def add_to_wishlist(request, product_variant_id):
#     product_variant = ProductVariant.objects.get(id=product_variant_id)
#     product = product_variant.product

#     # Check if the product is already in the user's wishlist
#     wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product_variant=product_variant)

#     if created:
#         message = f"{product.name, product_variant.name} added to wishlist successfully"
#     else:
#         wishlist_item.delete()
#         message = f"{product.name, product_variant.name} removed from wishlist successfully"

#     # Return a JSON response
#     return JsonResponse({'message': message})



        
def product_variant_details(request, product_variant_id):
    current_page = 'product-variant-details'
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    product = product_variant.product
    product_variants = ProductVariant.objects.filter(product=product)
    
    # Corrected line to get products related to the category and exclude the current product
    category_products = product.category.product_set.exclude(id=product_variant.product.id)


    if request.user.is_authenticated:
        product_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_variant', flat=True)
    else:
        product_wishlist = None
    
    context = {
        'current_page' : current_page,
        'product_variant' : product_variant,
        'product': product,
        'product_variants': product_variants,
        'current_product_variant_id': product_variant_id,
        'category_products' : category_products,
        'product_wishlist' : product_wishlist
    }
    return render(request, 'user/pages/product-variant-details.html', context)

def shop(request):
    current_page = 'shop'
    products = Product.objects.all()
    context = {
        'current_page': current_page,
        'products' : products
    }
    return render(request, 'user/pages/shop.html', context)

def offer_product(request):
    current_page = 'offer-product'
    offer_products = OfferProduct.objects.all()
    context = {
        'current_page': current_page,
        'offer_products' : offer_products
    }
    return render(request, 'user/pages/offer-product.html', context)

def category_products(request, category_id):
    current_page = 'category-product'

    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'current_page': current_page,
        'category': category,
        'products': products
    }
    return render(request, 'user/pages/category-products.html', context)






def cart(request):
    current_page = 'cart'
    user = request.user
    carts = Order_Item.objects.filter(user=user, order_status='CARTED')

    
    if request.user.is_authenticated:
        product_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_variant', flat=True)
    else:
        product_wishlist = None

    # Calculations
    cart_total = sum(
        x.quantity * (x.product_variant.discount_price or x.product_variant.actual_price)
        for x in carts
    )
    # In this version, the or operator is used within the sum function to select the discount price if available, otherwise, it falls back to the actual price

    discount_price_total = sum(x.quantity * (x.product_variant.discount_price or 0) for x in carts) 
    actual_price_total = sum(x.quantity * (x.product_variant.actual_price or 0) for x in carts) 
    discount = actual_price_total - discount_price_total

    if cart_total >= 50:
        delivery_charge = 0
    else:
        delivery_charge = 8

    total_amount = cart_total + delivery_charge

    
    context = {
        'current_page': current_page,
        'carts' : carts,
        'cart_total' : cart_total,
        'product_wishlist' : product_wishlist,
        'actual_price_total' : actual_price_total,
        'discount' : discount,
        'delivery_charge' : delivery_charge,
        'total_amount' : total_amount

    }
    return render(request, 'user/pages/cart.html', context)


def increase_quantity(request, cart_id):
    cart = Order_Item.objects.get(id=cart_id)
    cart.quantity += 1
    cart.save()
    return redirect('cart')


def decrease_quantity(request, cart_id):
    cart = Order_Item.objects.get(id=cart_id)
    if cart.quantity > 1: # make sure the quantity doesn't go below 1.
        cart.quantity -= 1  
        cart.save()
    return redirect('cart')


def delete_cart(request, cart_id):
    cart = Order_Item.objects.get(id=cart_id)
    cart.delete()
    return redirect('cart')

def checkout(request):
    user = request.user
    place_orders = Place_Order.objects.filter(user=user)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address') or None
        district = request.POST.get('district') or None
        place = request.POST.get('place') or None
        pin_code = request.POST.get('pin_code') or None
        phone = request.POST.get('phone') or None
        email = request.POST.get('email') or None
        
        place_order = Place_Order(
            user=user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            district=district,
            place=place,
            pin_code=pin_code,
            phone=phone,
            email=email,
        )
        place_order.save()
        messages.success(request, "addded")
        return redirect('checkout')
    
    context = {
        
        'place_orders' : place_orders,
    }

    return render(request, 'user/pages/checkout.html', context)

# @csrf_exempt
def payment(request, place_order_id):
    try:
        place_order = Place_Order.objects.get(id=place_order_id)
    except Place_Order.DoesNotExist:
        messages.error(request, 'Please select a address')
        return redirect('checkout')
    
    user = request.user
    carts = Order_Item.objects.filter(user=user, order_status='CARTED')


    #updating the carts
    for cart in carts:
        cart.place_order = place_order
        cart.actual_price_dummy = cart.product_variant.actual_price
        cart.discount_price_dummy = cart.product_variant.discount_price
        cart.save() 

    # Calculation
    cart_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(x.actual_price_dummy))
        for x in carts
    )
    discount_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(0))
        for x in carts
    )
    actual_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.actual_price_dummy) or Decimal(0))
        for x in carts
    )
    discount = actual_price_total - discount_price_total

    if cart_total >= 50:
        delivery_charge = 0
    else:
        delivery_charge = 8

    total_amount = cart_total + delivery_charge


    total_in_cents = int(total_amount * 100) 

    try:
        
        import razorpay
        client = razorpay.Client(auth=("rzp_test_GGmhwGLGUs22Xl", "S4E3s9dTwAywz2GB1waFFnnY")) #Key ID, Secret ID

        # Generate a unique identifier using UUID
        import uuid
        receipt_id = str(uuid.uuid4())

        data = { "amount":  total_in_cents , "currency": "INR", "receipt": receipt_id }
        payment = client.order.create(data=data)
        print(payment)
    except Exception as e:
        messages.error(request, 'Connection Field, PLease Check Your Network Connection')
        return redirect('checkout')

    # from datetime import datetime, timezone

    # payment_instance = Payment.objects.create(
    #     user=user,
    #     payment_id=payment['id'],
    #     entity=payment['entity'],
    #     currency=payment['currency'],
    #     receipt=payment['receipt'],
    #     notes=payment['notes'],
    #     created_at=datetime.utcfromtimestamp(payment['created_at']).replace(tzinfo=timezone.utc)
    # )
    # for cart in carts:
    #     payment_instance.order_item.add(cart)



    context = {
        'carts' : carts,
        'place_order' : place_order,
        'cart_total' : cart_total,
        'actual_price_total' : actual_price_total,
        'discount' : discount,
        'delivery_charge' : delivery_charge,
        'total_amount' : total_amount,
        'payment' : payment,
        'user' : user
    }
    

    return render(request, 'user/pages/payment.html', context)

@csrf_exempt
def payment_success(request):
    user = request.user
    carts = Order_Item.objects.filter(user=user, order_status='CARTED')

    # Calculation
    cart_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(x.actual_price_dummy))
        for x in carts
    )
    discount_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(0))
        for x in carts
    )
    actual_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.actual_price_dummy) or Decimal(0))
        for x in carts
    )
    discount = actual_price_total - discount_price_total

    if cart_total >= 50:
        delivery_charge = 0
    else:
        delivery_charge = 8

    total_amount = cart_total + delivery_charge

    
    payment = Payment.objects.create(
        user=user,
        cart_total=cart_total,
        discount=discount,
        delivery_charge=delivery_charge,
        total_amount=total_amount,
        payment_status='SUCCESS'
    )
    for cart in carts:
        payment.order_item.add(cart)

    carts.update(order_status='PAID')
    

    return render(request, 'user/pages/payment-success.html')

@csrf_exempt
def payment_field(request):
    user = request.user
    carts = Order_Item.objects.filter(user=user, order_status='CARTED')

    # Calculation
    cart_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(x.actual_price_dummy))
        for x in carts
    )
    discount_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.discount_price_dummy) or Decimal(0))
        for x in carts
    )
    actual_price_total = sum(
        Decimal(x.quantity) * (Decimal(x.actual_price_dummy) or Decimal(0))
        for x in carts
    )
    discount = actual_price_total - discount_price_total

    if cart_total >= 50:
        delivery_charge = 0
    else:
        delivery_charge = 8

    total_amount = cart_total + delivery_charge

    
    payment = Payment.objects.create(
        user=user,
        cart_total=cart_total,
        discount=discount,
        delivery_charge=delivery_charge,
        total_amount=total_amount,
        payment_status='FIELD'
    )
    for cart in carts:
        payment.order_item.add(cart)

    # carts.update(order_status='')
    

    return render(request, 'user/pages/payment-field.html')








