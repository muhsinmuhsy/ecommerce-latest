from admin_app.models import Category
from user_app.models import *

def context(request):
    if request.user.is_authenticated:
        # cart_count = Order_Item.objects.filter(user=request.user, order_status='CARTED').count()
        carted = Order_Item.objects.filter(user=request.user, order_status='CARTED')

        cart_count = sum(item.quantity for item in carted)
    else:
        cart_count = 0
    context = {
        'cart_count' : cart_count
    }
    return context