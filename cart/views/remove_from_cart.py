from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from cart.services import CartService


class RemoveFromCartView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            CartService.remove_from_cart(request.user, product_id)
        else:
            CartService.remove_from_session_cart(request.session, product_id)

        messages.success(request, "Item removed from cart")
        return redirect('store:cart_detail')