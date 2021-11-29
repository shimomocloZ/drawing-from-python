import dataclasses

from src.models.wishlist import Wishlist

@dataclasses.dataclass
class Buyer:
    id: int = 0
    name: str = ''
    wishlist: Wishlist = None

    def __post_init__(self):
        self.id = int(self.id)
        self.wishlist = self.make_wishlist(self.wishlist)

    def make_wishlist(self, wishlist: dict) -> Wishlist:
        return Wishlist(**wishlist)
