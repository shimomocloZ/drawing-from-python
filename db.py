
from migrations.models.buyer import Buyers
from migrations.models.product import Products
from migrations.models.reserved_product import ReservedProducts
from migrations.models.wishlist import Wishlists
from migrations.setting import Session


def main():
    # εε
    # insert
    # product = Products()
    # product.name = 'A'
    # Session.add(product)
    # Session.commit()
    # select *
    select_products = Products.query.all()
    for product in select_products:
        print(product.id, product.name)

    # select * where
    select_products = Products.query.filter_by(id=1)
    for product in select_products:
        print(product.id, product.name)

    select_products = Products.query.filter(Products.id != 1)
    for product in select_products:
        print(product.id, product.name)

    # wishlist
    # wishlist = Wishlists()
    # wishlist.priority = 'A;B'
    # wishlist.number_of_buy = '1;1'
    # Session.add(wishlist)

    wishlists = Wishlists.query.all()
    for res in wishlists:
        print(res.id, res.priority, res.number_of_buy)

    # buyer = Buyers()
    # buyer.name = 'δΌθ€'
    # buyer.wishlist_id = wishlists[0].id
    # Session.add(buyer)

    buyers = Buyers.query.all()
    for res in buyers:
        print(res.id, res.name, res.wishlist_id)

    reserved_products = ReservedProducts.query.all()
    for res in reserved_products:
        print(res.id, res.product_name, res.buyer_name)


if __name__ == '__main__':
    main()
