from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from cart.services import CartService
from store.forms import ProductQuantityForm
from store.models import Product


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        form = ProductQuantityForm(request.POST)

        if form.is_valid():
            product = get_object_or_404(Product, id=form.cleaned_data['product_id'])
            quantity = form.cleaned_data['quantity']

            if request.user.is_authenticated:
                CartService.add_to_cart(
                    user=request.user,
                    product=product,
                    quantity=quantity
                )
            else:
                CartService.add_session_cart(
                    session=request.session,
                    product=product,
                    quantity=quantity
                )

        messages.success(request, 'Successfully added to cart')
        return redirect('store:cart_detail')
