from django.shortcuts import render
from django.views.generic import View
from cart.services import CartService


class CartDetailView(View):
    def get(self, request):
        cart_items = CartService.get_cart_items(request)
        return render(request, 'store/cart_detail.html', {'cart_items': cart_items})