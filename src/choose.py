# -*- coding: utf-8 -*-
import logging
import random

from migrations.models.buyer import Buyers
from migrations.models.product import Products
from migrations.models.wishlist import Wishlists  # noqa E401

log = logging.getLogger()


def main():
    # 購入者を取得
    buyers: list[Buyers] = Buyers.query.all()
    # 商品
    products: list[Products] = Products.query.all()

    # 抽選処理
    # 商品ごとに購入優先度を設定する
    drawings: dict = {product.name: [] for product in products}

    for buyer in buyers:
        # 購入優先度を取得
        wishlist: Wishlists = buyer.wishlist
        priorities = convert_priority(wishlist.priority)
        numbers_of_buy = convert_number_of_buy(wishlist.number_of_buy)
        for product_name, num_of_buy in zip(priorities, numbers_of_buy):
            print(product_name, num_of_buy)
            # バリデーション
            # 商品に存在しないものは弾く
            if not validate_product(product_name, products):
                log.warning(
                    f'選択した商品は存在しません。 購入者={buyer.name}, 商品名={product_name}')
                continue

            # 購入数が多いものは弾く
            if not validate_buy_of_num(num_of_buy):
                log.warning(
                    f'商品2つまでしか購入できません。購入者={buyer.name}, 購入数={num_of_buy}')
                continue

            drawings[product_name].append({
                'buyer': buyer.name,
                'number_of_buy': num_of_buy
            })

    drawing_result: dict = {product.name: [] for product in products}
    # 購入優先度順にソート
    for key in drawings:
        # 商品の購入者がいない場合はスキップ
        if len(drawings[key]) == 0:
            # 結果からも消す
            del drawing_result[key]
            continue
        max_number = max(drawings[key], key=lambda x: x['number_of_buy'])[
            'number_of_buy']
        min_number = min(drawings[key], key=lambda x: x['number_of_buy'])[
            'number_of_buy']
        buyers_of_product = drawings[key]
        # 最大値と最小値が混在している場合は最大値をリストから除去する
        if max_number != min_number:
            buyers_of_product = [buyer for buyer in drawings[key]
                                 if buyer['number_of_buy'] == min_number]

        # 1人のみに絞れた場合は終了する
        if len(buyers_of_product) == 1:
            drawing_result[key] = buyers_of_product
            continue

        # 対象者が複数人いる場合は、ランダム選出
        random_buyers = random.sample(
            buyers_of_product, len(buyers_of_product))
        # 2回抽選
        drawing_result[key] = random_buyers[random.randrange(
            len(random_buyers))]

    # TODO 確定枠を作成
    # ダンプ
    import json
    print(json.dumps(drawing_result, ensure_ascii=False, indent=2))


def validate_product(product_name, product_models: list[Products]):
    result = [p.name for p in product_models if p.name == product_name]
    return len(result) != 0


def validate_buy_of_num(num_of_buy):
    return num_of_buy <= 2


def convert_priority(priority: str):
    return priority.split(';')


def convert_number_of_buy(number_of_buy: str):
    if ';' not in number_of_buy:
        return [int(number_of_buy)]

    return [int(num) for num in number_of_buy.split(';')]
