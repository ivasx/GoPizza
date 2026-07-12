from dataclasses import dataclass

from store.models import Product


@dataclass
class CartItemDTO:
    product: Product
    quantity: int

    @property
    def get_total(self):
        return self.product.price * self.quantity