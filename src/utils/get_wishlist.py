
def get_wishlist(wish_list_id: str, wishlists: list[dict]) -> dict:
    for wishlist in wishlists:
        if wishlist['id'] == wish_list_id:
            return wishlist
