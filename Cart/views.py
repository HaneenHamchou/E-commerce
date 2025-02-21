from django.shortcuts import render # type: ignore
from Cart.models import Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    response = render(request, "cart/index.html", {'products':products})
    return response