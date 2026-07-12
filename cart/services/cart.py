from django.shortcuts import get_object_or_404

from store.models import Product
from .cart_item_dto import CartItemDTO
from ..models import Cart, CartItem


class CartService:
    @staticmethod
    def add_to_cart(user, product, quantity):
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    @staticmethod
    def add_session_cart(session, product, quantity):
        cart_data = session.get('cart_data', {})
        product_id = str(product.id)

        if product_id in cart_data:
            cart_data[product_id] += quantity
        else:
            cart_data[product_id] = quantity

        session['cart_data'] = cart_data
        session.modified = True

    @staticmethod
    def merge_session_cart_to_db(request, user):
        session_cart = request.session.get('cart_data', {})
        if not session_cart:
            return

        cart, _ = Cart.objects.get_or_create(user=user)
        for product_id, quantity in session_cart.items():
            product = get_object_or_404(Product, id=product_id)
            CartService.add_to_cart(user, product, quantity)

        request.session['cart_data'] = {}

    @staticmethod
    def get_cart_items(request):
        items = []
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            for item in cart.items.all():
                items.append(CartItemDTO(product=item.product, quantity=item.quantity))
        else:
            cart_data = request.session.get('cart_data', {})
            for product_id, quantity in cart_data.items():
                product = Product.objects.get(id=product_id)
                items.append(CartItemDTO(product=product, quantity=quantity))

        return items